from datetime import datetime
from flask import Blueprint
from flask_login import current_user
from flask_restful import Resource, marshal_with, Api, abort
from pony.orm import commit
from pony.orm import select, desc
from webargs.flaskparser import use_args, use_kwargs

from ..aws import create_submission_presigned_post
from ..fields_req import contest_args, pagination_args, contest_team_args, merge_request_args, submission_args
from ..fields_res import contest_fields, contest_basic_fields, team_basic_fields, team_member_fields, team_fields, \
    merge_request_fields, submission_fields
from ..models import Contest, MergeRequest, Participation, Submission, User
from ..utils import handle_db_errors, require_login, require_my_team, require_object


class ContestResource(Resource):
    @require_object(Contest)
    @marshal_with(contest_fields)
    def get(self, contest):
        return contest

    @require_object(Contest)
    def delete(self, contest):
        contest.delete()
        return '', 204

    @require_object(Contest)
    @use_args(contest_args(is_post=False))
    @marshal_with(contest_fields)
    def patch(self, args, contest):
        contest.set(**args)
        commit()
        return contest, 202


class ContestListResource(Resource):
    @marshal_with(contest_basic_fields)
    @use_kwargs(pagination_args)
    def get(self, limit, offset):
        return list(select(c for c in Contest)
                    .order_by(desc(Contest.weight))[offset:offset + limit])

    @use_args(contest_args(is_post=True))
    @marshal_with(contest_fields)
    def post(self, args):
        contest = Contest(**args)
        commit()
        return contest, 201


class ContestTeamResource(Resource):
    @require_object(Participation, 'team_id')
    @require_object(Contest)
    @marshal_with(team_fields)
    def get(self, contest, participation):
        if participation.team_leader is not None:
            abort(404)  # record exists but does not represent a team
        return participation

    @marshal_with(team_basic_fields)
    @require_object(Participation, 'team_id')
    @require_object(Contest)
    @use_args(contest_team_args)
    def put(self, args, contest, participation):
        participation.set(**args)
        return participation, 202


class ContestTeamListResource(Resource):
    @marshal_with(team_basic_fields)
    @use_kwargs(pagination_args)
    @require_object(Contest)
    def get(self, contest, limit, offset):
        teams = list(select(
            p for p in Participation
            if p.contest.id == contest.id and p.is_leader
        )[offset:offset + limit])
        return teams

    @require_object(Contest)
    @use_args(contest_team_args)
    @marshal_with(team_basic_fields)
    @require_login
    def post(self, args, contest):
        participation = Participation(user=User[current_user.id], contest=contest, **args)
        commit()
        return participation


class ContestTeamMemberListResource(Resource):
    @marshal_with(team_member_fields)
    @require_object(Participation, 'team_id')
    @require_object(Contest)
    def get(self, contest, participation):
        return list(participation.team_members)


class MergeTeamResource(Resource):
    @require_object(Contest)
    @marshal_with(merge_request_fields)
    @use_args(merge_request_args)
    @require_login
    def post(self, args, contest):
        args['src_team'] = Participation.get_team_by_user(contest, current_user.id, True) or abort(403)
        args['tgt_team'] = Participation.get_team_in_contest(contest.id, args['tgt_team']) or abort(404)
        print(args['tgt_team'])
        if args['src_team'].id == args['tgt_team'].id:
            abort(422)

        merge_request = MergeRequest(**args)
        commit()
        return merge_request, 201

    @require_object(Contest)
    @require_my_team(is_leader=True)
    def delete(self, contest, my_team):
        merge_request = MergeRequest.from_team(my_team) or abort(404, error='error_resource_not_found')
        merge_request.delete()
        return '', 204

    @require_object(Contest)
    @require_my_team(is_leader=True)
    @marshal_with(merge_request_fields)
    def get(self, contest, my_team):
        return MergeRequest.from_team(my_team) or abort(404, error='error_resource_not_found')


class MyTeamResource(Resource):
    @require_object(Contest)
    @require_my_team()
    @marshal_with(team_basic_fields)
    @require_login
    def get(self, contest, my_team):
        return my_team


class MyTeamMergeRequestResource(Resource):
    @require_object(Contest)
    @require_my_team(is_leader=True)
    @marshal_with(merge_request_fields)
    @require_login
    def get(self, contest, my_team):
        """list of merge requests sent by other teams"""
        return list(MergeRequest.to_team(my_team))


class MyTeamMergeRequestAcceptResource(Resource):
    @require_object(Contest)
    @require_my_team(is_leader=True)
    @require_object(MergeRequest, src_field="merge_request_id", tgt_field="merge_request")
    @marshal_with(team_basic_fields)
    @require_login
    def post(self, contest, my_team, merge_request):
        """accept a merge request"""
        if merge_request.tgt_team != my_team:
            abort(403, error='error_unauthorized')
        merge_request.accept()
        # change leader or src_team
        # TODO: bulk update
        for participation in merge_request.src_team.team_members:
            participation.team_leader = my_team

        return merge_request.tgt_team, 201


class MyTeamMergeRequestRejectResource(Resource):
    @require_object(Contest)
    @require_my_team(is_leader=True)
    @require_object(MergeRequest, src_field="merge_request_id", tgt_field="merge_request")
    @require_login
    def post(self, contest, my_team, merge_request):
        """reject a merge request"""
        if merge_request.tgt_team != my_team:
            abort(403, error='error_unauthorized')
        merge_request.reject()
        return '', 201


class ContestSubmissionResource(Resource):
    @require_login
    @require_object(Contest)
    @use_kwargs(pagination_args)
    @marshal_with(submission_fields)
    def get(self, contest, limit, offset):
        participation = Participation.get_team_by_user(contest, current_user.id) or abort(404)
        # get all submissions of team
        submissions = list(select(
            s for s in Submission
            if s.participation in participation.team_members
        ).order_by(desc(Submission.id))[offset:offset + limit])

        return submissions

    @require_login
    @require_object(Contest)
    @use_args(submission_args)
    def post(self, args, contest):
        participation = Participation.get_team_by_user(contest, current_user.id) or abort(404)
        # check submission limit
        if participation.num_submissions_today >= contest.num_allow_submissions_perday:
            abort(429, error='error_submissions_per_day_limit_exceeded')

        # save new record
        submission = Submission(
            participation=participation,
            created_at=datetime.utcnow(),
            **args
        )
        commit()

        return create_submission_presigned_post(
            contest.id,
            participation.id,
            submission.id
        )


bp = Blueprint('contests', __name__, url_prefix='/contests')


api = Api(bp, decorators=[handle_db_errors])
api.add_resource(ContestResource, '/<int:contest_id>')
api.add_resource(ContestListResource, '')
api.add_resource(ContestTeamResource, '/<int:contest_id>/teams/<int:team_id>')
api.add_resource(ContestTeamListResource, '/<int:contest_id>/teams')
api.add_resource(ContestTeamMemberListResource, '/<int:contest_id>/teams/<int:team_id>/members')
api.add_resource(MyTeamResource, '/<int:contest_id>/teams/my-team')
api.add_resource(MergeTeamResource, '/<int:contest_id>/teams/my-team/merge')
api.add_resource(MyTeamMergeRequestResource, '/<int:contest_id>/teams/my-team/merge-requests')
api.add_resource(MyTeamMergeRequestAcceptResource,
                 '/<int:contest_id>/teams/my-team/merge-requests/<int:merge_request_id>/accept')
api.add_resource(MyTeamMergeRequestRejectResource,
                 '/<int:contest_id>/teams/my-team/merge-requests/<int:merge_request_id>/reject')

api.add_resource(ContestSubmissionResource, '/<int:contest_id>/my-team/submissions')
