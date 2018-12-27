import json

from . import request, endpoint as ep


def test_ping(client):
    res = client.get('/ping')
    assert b'pong' in res.data


def test_reject_wrong_email():
    user = dict(username='test.user', password='123456', email="test_at_mail.com")
    with request.post('/users', data=user, expected_status_code=400) as res:
        assert res.get('error') == 'error_params'


def test_reject_missing_email_field():
    user = dict(username='test.user', password='123456')
    with request.post('/users', data=user, expected_status_code=400) as res:
        assert res.get('error') == 'error_params'


def test_reject_existing_email():
    user = dict(username='test.user2', password='123456', email="test2@mail.com")
    with request.post('/users', data=user) as u:
        assert u['user_id']
    with request.post('/users', data=user, expected_status_code=422) as res:
        assert res.get('error') == 'error_transaction_integrity'


def test_create_user_and_login():
    user = dict(username='test.user', password='123456', email="test@mail.com")
    with request.post('/users', data=user) as u:
        assert u['user_id']

    with request.get('/me', user=user) as u:
        assert u['username'] == user['username']


def test_wrong_username_or_password_login(client):
    for username, password in [
        ('unknown', 'whatever'),
        ('user1', 'wrong11'),
    ]:
        with client.post(
            ep.USER_LOGIN, data={'username': username, 'password': password}
        ) as res:
            assert res.status_code == 422
            assert json.loads(res.data).get('error') == 'error_wrong_username_or_password'


def test_unathorized():
    with request.get('/me') as res:
        assert res.get('error') == 'error_unauthorized'
