from . import request
from . import endpoint as ep


def test_users():
    with request.get(ep.USER_LIST) as users:
        assert len(users) == 6
        assert users[0].keys() >= {'id', 'username'}

    with request.get(ep.USER_GET % 1) as user:
        assert user['username'] == 'user1'

    with request.get(ep.USER_GET_BY_USERNAME % 'user2') as user:
        assert user['id'] == 2

    with request.get(ep.MY_PROFILE, user=dict(username='user1', password='password')) as user:
        assert user['username'] == 'user1'

    with request.patch(ep.MY_PROFILE,
                       user=dict(username='user1', password='password'),
                       data=dict(bio='new bio')) as user:
        assert user['bio'] == 'new bio'
