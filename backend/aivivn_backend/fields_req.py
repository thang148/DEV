from marshmallow import validate
from webargs.fields import Str, Int

pagination_args = {
    'limit': Int(missing=10),
    'offset': Int(missing=0)
}

login_args = {
    'username': Str(required=True, validate=validate.Regexp(r'^[a-zA-Z0-9_.]{4,64}$')),
    'password': Str(required=True, validate=validate.Length(6))
}

signup_args = {
    **login_args,
    'email': Str(required=True, validate=validate.Email()),
}


def contest_args(is_post=True):
    return {
        'title': Str(required=is_post),
        'subtitle': Str(required=is_post),
        'description': Str(),
        'evaluation': Str(),
        'prizes': Str(),
        'timeline': Str(),
        'weight': Int(),
    }


user_me_args = {
    'bio': Str()
}


contest_team_args = {
    'name': Str(required=True, attribute='team_name')
}

merge_request_args = {
    'tgt_team': Int(required=True),
    'message': Str()
}

submission_args = {
    'note': Str()
}
