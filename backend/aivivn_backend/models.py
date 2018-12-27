from datetime import datetime, date
import hashlib

import bcrypt
import jwt
from flask import current_app
from flask_login import UserMixin
from pony.orm import Database, Required, Optional, Set, Json, composite_key, count, select, composite_index, max

from .aws import create_contest_label_key
from .cache import cache
from .constants import NULL_DATETIME

db = Database()


class UpdateDateTimeMixin():
    def before_update(self):
        self.updated_at = datetime.utcnow()


class CacheableMixin():
    def __repr__(self):
        """
        unique key for caching
        :return:
        """
        return "%s(%s)" % (self.__class__.__name__, self.id)


class User(UserMixin, db.Entity):
    username = Required(str, unique=True)
    email = Required(str, unique=True)

    bio = Optional(str)

    timezone = Optional(str)

    hashed_password = Required(str)
    last_login = Optional(datetime)
    participations = Set('Participation')

    ranking_point = Optional(int, default=0)

    # created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    # updated_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        super(User, self).__init__(
            hashed_password=self.hash_password(password),
            **kwargs
        )

    @property
    def avatar(self):
        email = (self.email or self.username).encode('utf-8')
        size = 256
        gravatar_url = (
            'https://secure.gravatar.com/avatar' +
            f'/{hashlib.md5(email.lower()).hexdigest()}?s={size}&d=identicon'
        )
        return gravatar_url

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        ).decode('ascii')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.hashed_password.encode('utf-8')
        )

    def generate_token(self):
        return jwt.encode(
            {'user_id': self.id},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('ascii')

    @classmethod
    def get_user_from_token(cls, token):
        try:
            payload = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return cls[payload['user_id']]
        except jwt.PyJWTError:
            return None

    @property
    def global_rank(self):
        return 5  # TODO: value here


class Contest(UpdateDateTimeMixin, CacheableMixin, db.Entity):
    title = Required(str)
    subtitle = Optional(str)

    description = Optional(str)
    evaluation = Optional(str)
    prizes = Optional(str)
    timeline = Optional(str)

    participations = Set("Participation")

    start_date = Optional(datetime)
    end_date = Optional(datetime)

    weight = Optional(int)  # listing priority

    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    updated_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')

    @property
    def status(self):
        return "undefined"

    @property
    @cache.memoize()
    def num_allow_submissions_perday(self):
        return 5

    @property
    # @cache.memoize()
    def num_teams(self):
        return int(count(p for p in Participation if p.is_leader and p.contest == self))

    @property
    @cache.memoize()
    def num_submissions(self):
        return int(count(s for s in Submission if s.participation.contest.id == self.id))

    @property
    def scoring_meta(self):
        label_type = int
        return {
            'public': create_contest_label_key(self.id, public=True),
            'private': create_contest_label_key(self.id, public=False),
            'id': 'filename',
            'label': 'label',
            'label_type': label_type,
            'evaluator_name': 'AccuracyEvaluator',
        }


class MergeRequest(db.Entity):
    src_team = Required("Participation", reverse="merge_requests")
    tgt_team = Required("Participation")
    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')

    accepted_at = Required(datetime, default=NULL_DATETIME)
    rejected_at = Required(datetime, default=NULL_DATETIME)

    composite_key(src_team, rejected_at)

    message = Optional(str)

    def reject(self):
        self.rejected_at = datetime.utcnow()

    def accept(self):
        self.accepted_at = datetime.utcnow()

    @classmethod
    def to_team(cls, team):
        return select(
            mr for mr in MergeRequest
            if mr.tgt_team == team
        )

    @classmethod
    def from_team(cls, team):
        return select(
            mr for mr in MergeRequest
            if mr.src_team == team
        ).first()

    @property
    def status(self):
        if self.rejected_at != NULL_DATETIME:
            return "rejected"
        elif self.accepted_at != NULL_DATETIME:
            return "accepted"
        else:
            return "pending"


class Participation(UpdateDateTimeMixin, db.Entity):
    user = Required(User)
    contest = Required(Contest)
    composite_key(user, contest)

    submissions = Set("Submission")

    team_name = Optional(str)
    team_leader = Optional("Participation", reverse="team_other_members")
    composite_index(contest, team_leader)
    composite_key(contest, team_name)

    team_other_members = Set("Participation", reverse="team_leader")
    team_info = Optional(Json)

    merge_requests = Set("MergeRequest", reverse="src_team")
    _merge_request = Optional("MergeRequest", reverse="tgt_team")  # unused

    last_week_rank = Optional(int)

    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    updated_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')

    @property
    def team_members(self):
        team_leader = self if self.is_leader else self.team_leader
        return team_leader.team_other_members + [team_leader]

    @classmethod
    def get_team_in_contest(cls, contest_id, team_id):
        return select(
            p for p in Participation
            if p.contest.id == contest_id
            and p.is_leader
            and p.id == team_id
        ).first()

    @classmethod
    def get_team_by_user(cls, contest, user_id, is_leader=False):
        p = select(
            p for p in Participation
            if p.contest == contest
            and p.user.id == user_id
        ).first()
        if not p or (is_leader and not p.is_leader):
            return None
        return p if p.is_leader else p.team_leader

    @classmethod
    def select_teams(cls, **kwargs):
        return select(
            p for p in Participation
            if p.contest.id == kwargs['contest_id']
            and p.is_leader
            and p.user.id == kwargs['leader_id']).first()

    @classmethod
    def public_leaderboard(cls, contest_id):
        # TODO: cache and invalidate when score of a team change
        teams = select(
            p for p in Participation
            if p.contest.id == contest_id
            and p.is_leader
        )
        return [
            p.id for p in
            sorted(teams, key=lambda p: p.public_score, reverse=True)
        ]

    @property
    def rank(self):
        return self.public_leaderboard(self.contest.id).index(self.id) + 1

    @property
    def is_leader(self):
        return self.team_leader is None

    @property
    def num_submissions_today(self):
        return count(
            s for s in Submission
            if s.participation in self.team_members
            and s.created_at.date() == date.today()
        )

    @property
    def public_score(self):
        return max(
            s.public_score for s in Submission
            if s.participation in self.team_members
            and s.created_at.date() == date.today()
        ) or 0

    @property
    def num_submissions(self):
        if not self.is_leader:
            return 0
        return int(count(
            s for s in Submission
            if s.participation in self.team_members
        ))

    @property
    def last_submission_at(self):
        return max(
            s.created_at for s in Submission
            if s.participation in self.team_members
        )


class Submission(UpdateDateTimeMixin, db.Entity):
    participation = Required(Participation)
    private_score = Optional(float)
    public_score = Optional(float)
    comment = Optional(str)
    note = Optional(str)

    created_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    updated_at = Required(datetime, sql_default='CURRENT_TIMESTAMP')
