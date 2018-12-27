from . import endpoint as ep
from . import request


def test_teams():
    contest_id = 1

    data = {'name': 'test'}

    request.get(ep.TEAM_LIST % 3, data=data, user_id=1, expected_status_code=200)

    with request.get(ep.TEAM_LIST % contest_id) as teams:
        assert len(teams) == 3
        assert teams[0].keys() >= {'name', 'leader'}
        assert len(teams[0]['members']) == 3

    with request.get(ep.TEAM_GET % (contest_id, teams[0]['id'])) as team:
        assert team.keys() >= {'name', 'leader'}
        assert team['name'] == 'team1'

    with request.put(ep.TEAM_GET % (contest_id, teams[0]['id']), data=dict(name="new name")):
        with request.get('/contests/%s/teams/%s' % (contest_id, teams[0]['id'])) as team:
            assert team['name'] == 'new name'

    with request.get(ep.TEAM_MEMBER_LIST % (contest_id, teams[0]['id'])) as members:
        assert len(members) == 3
        assert members[0].keys() >= {'id', 'username'}
