from flask_restful.fields import Integer, String, DateTime, Nested, List, Url, Float

timestamp_fields = {
    'updated_at': DateTime,
    'created_at': DateTime,
}

contest_basic_fields = {
    'id': Integer,
    'title': String,
    'subtitle': String,
    'status': String,
    'num_teams': Integer,
    # 'num_submissions': Integer,
    **timestamp_fields,
}

contest_fields = {
    **contest_basic_fields,
    'description': String,
    'evaluation': String,
    'prizes': String,
    'timeline': String,
    'weight': Integer
}

user_basic_fields = {
    'id': Integer,
    'username': String,
    'avatar': String,
    # **timestamp_fields,
}

user_fields = {
    **user_basic_fields,
    'bio': String,
}

user_me_fields = {
    **user_fields,
}

team_member_fields = {
    'id': Integer,
    'username': String(attribute='user.username'),
    'user_id': Integer(attribute='user.id'),
    **timestamp_fields,
}

team_basic_fields = {
    'id': Integer,
    'rank': Integer,
    'name': String(attribute='team_name'),
    'leader': Integer(attribute='user.id'),
    'members': List(Nested(team_member_fields), attribute='team_members'),
    'public_score': Float,
    # 'private_score': Float,
    'last_submission_at': DateTime,
    'num_submissions': Integer,
    **timestamp_fields,
}

team_fields = {
    **team_basic_fields,
}

merge_request_fields = {
    'id': Integer,
    'src_team': Integer(attribute='src_team.id'),
    'tgt_team': Integer(attribute='tgt_team.id'),
    'status': String,
    **timestamp_fields,
}

submission_fields = {
    'id': Integer,
    'public_score': Float,
    # 'private_score': Float,
    'file': String,
    'comment': String,
    'note': String,
    **timestamp_fields,
}

create_submission_fields = {
    'url': Url,
    'fields': Nested,
}
