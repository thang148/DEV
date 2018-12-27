from . import request
from . import endpoint as ep
from .utils import mark_as_dirty


@mark_as_dirty
def test_team_actions():
    contest_id = 2
    src_team = 1
    tgt_team = 2

    with request.get(ep.MY_TEAM % contest_id, user_id=1) as team:
        assert team.keys() >= {'id', 'name', 'leader'}
        assert any(mem['username'] == "user1" for mem in team['members'])

    # send merge request
    with request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id,
                      user_id=1, data=dict(tgt_team=tgt_team), expected_status_code=201) as mr:
        mr_id = mr['id']
        # test merge request appearing in list
        with request.get(ep.MERGE_REQUEST % contest_id, user_id=2) as merge_requests:
            assert len(merge_requests) == 1

        # test merge request field
        with request.get(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1) as merge_request:
            assert merge_request.get('id') == mr_id
            assert merge_request.keys() >= {'id', 'src_team', 'tgt_team'}

        # test deleting merge request
        with request.delete(
                ep.OUTBOUND_MERGE_REQUEST % contest_id,
                user_id=1,
                expected_status_code=204):
            with request.get(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                             expected_status_code=404):
                pass


@mark_as_dirty
def test_accepting_request():
    contest_id = 2
    src_team = 1
    tgt_team = 2
    # test accepting request
    with request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                      data=dict(tgt_team=tgt_team), expected_status_code=201):
        with request.post(ep.MERGE_REQUEST_ACCEPT % (contest_id, src_team),
                          user_id=2, expected_status_code=201) as new_team:
            assert len(new_team['members']) == 2

        # test src_team no longer exists
        request.get(ep.TEAM_GET % (contest_id, src_team), user_id=2, expected_status_code=404)


@mark_as_dirty
def test_rejecting_request():
    contest_id = 2
    src_team = 1
    tgt_team = 2
    with request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                      data=dict(tgt_team=tgt_team)) as merge_request:
        mr_id = merge_request['id']

        with request.post(ep.MERGE_REQUEST_REJECT % (contest_id, src_team),
                          user_id=2, expected_status_code=201):
            pass

        # test merge request rejected
        with request.get(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1) as merge_request:
            assert merge_request['status'] == "rejected"


@mark_as_dirty
def test_merge_request_to_2_different_teams():
    contest_id = 2
    tgt_team1 = 2
    tgt_team2 = 3

    request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                 data=dict(tgt_team=tgt_team1))
    request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                 data=dict(tgt_team=tgt_team2), expected_status_code=422)


@mark_as_dirty
def test_merge_request_to_same_team_twice():
    contest_id = 2
    tgt_team = 2

    request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                 data=dict(tgt_team=tgt_team))
    request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                 data=dict(tgt_team=tgt_team), expected_status_code=422)


def test_merge_request_from_non_leader():
    contest_id = 1
    tgt_team = 2

    request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=2,
                 data=dict(tgt_team=tgt_team), expected_status_code=403)


@mark_as_dirty
def test_merge_request_to_non_leader():
    contest_id = 2
    src_team = 1
    tgt_team = 2
    # test accepting request
    with request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=1,
                      data=dict(tgt_team=tgt_team), expected_status_code=201):
        with request.post(ep.MERGE_REQUEST_ACCEPT % (contest_id, src_team),
                          user_id=2, expected_status_code=201) as new_team:
            assert len(new_team['members']) == 2

        # test src_team no longer exists
        request.get(ep.TEAM_GET % (contest_id, src_team), user_id=2, expected_status_code=404)

    request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=3,
                 data=dict(tgt_team=src_team), expected_status_code=404)


def test_merge_request_to_non_existing_team():
    contest_id = 2
    tgt_team = 1000

    request.post(ep.OUTBOUND_MERGE_REQUEST % contest_id, user_id=3,
                 data=dict(tgt_team=tgt_team), expected_status_code=404)
