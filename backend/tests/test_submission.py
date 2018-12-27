from . import request
from . import endpoint as ep
from .utils import mark_as_dirty

# constest
contest_id = 1


def test_list_submissions_team1(client):
    with request.get(ep.SUBMISSION_LIST % contest_id, user_id=1) as submissions:
        assert len(submissions) == 7
        assert submissions[0]['id'] > submissions[1]['id'] > submissions[2]['id']

    with request.get(ep.SUBMISSION_LIST % contest_id, user_id=2) as submissions:
        assert len(submissions) == 7

    with request.get(ep.SUBMISSION_LIST % contest_id, user_id=3) as submissions:
        assert len(submissions) == 7


def test_list_submissions_team2(client):
    with request.get(ep.SUBMISSION_LIST % contest_id, user_id=4) as submissions:
        assert len(submissions) == 5

    with request.get(ep.SUBMISSION_LIST % contest_id, user_id=5) as submissions:
        assert len(submissions) == 5


def test_list_submissions_team3(client):
    with request.get(ep.SUBMISSION_LIST % contest_id, user_id=6) as submissions:
        assert len(submissions) == 3


@mark_as_dirty
def test_create_submission_team1_above_limit(client):
    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=1,
                      data=dict(note='test note'), expected_status_code=429) as msg:
        assert msg['error'] == 'error_submissions_per_day_limit_exceeded'

        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=1) as submissions:
            assert len(submissions) == 7

    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=2,
                      data=dict(note='test note'), expected_status_code=429):
        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=2) as submissions:
            assert len(submissions) == 7

    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=3,
                      data=dict(note='test note'), expected_status_code=429):
        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=3) as submissions:
            assert len(submissions) == 7


@mark_as_dirty
def test_create_submission_team2_equal_limit(client):
    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=4,
                      data=dict(note='test note')):
        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=4) as submissions:
            assert len(submissions) == 5

    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=5,
                      data=dict(note='test note'), expected_status_code=429):
        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=5) as submissions:
            assert len(submissions) == 5


@mark_as_dirty
def test_create_submission_team3(client):
    # 1st ==> total submissions: 4
    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=6,
                      data=dict(note='test note')) as presigned_post:
        assert presigned_post['url'].endswith('s3.amazonaws.com/')
        assert presigned_post['fields']['key'].startswith('submissions/')
        assert presigned_post['fields']['acl'] == 'authenticated-read'

        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=6) as submissions:
            assert len(submissions) == 4
            assert submissions[0]['note'] == 'test note'

    # 2nd ==> total submissions: 5 (LIMIT)
    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=6,
                      data=dict(note='test note 1')) as presigned_post:
        assert presigned_post['url'].endswith('s3.amazonaws.com/')
        assert presigned_post['fields']['key'].startswith('submissions/')
        assert presigned_post['fields']['acl'] == 'authenticated-read'

        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=6) as submissions:
            assert len(submissions) == 5
            assert submissions[0]['note'] == 'test note 1'

    # 3th ==> over
    with request.post(ep.SUBMISSION_CREATE % contest_id, user_id=6,
                      data=dict(note='test note 2'), expected_status_code=429):
        with request.get(ep.SUBMISSION_LIST % contest_id, user_id=6) as submissions:
            assert len(submissions) == 5
