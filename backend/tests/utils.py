import json
from functools import wraps

import pytest


def get_user_header(client, user_credential):
    if user_credential is None:
        return None
    with client.post('/users/login', data=user_credential) as res:
        access_token = json.loads(res.data)['access_token']
        return {
            'Authorization': 'Bearer {}'.format(access_token)
        }


def mark_as_dirty(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        pytest.is_dirty = True
        return f(*args, **kwargs)
    return decorated
