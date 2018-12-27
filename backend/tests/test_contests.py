from tests import request
from .utils import mark_as_dirty


@mark_as_dirty
def test_contests():
    with request.get('/contests', limit=3) as contests:
        assert len(contests) == 3
        assert {
            'id', 'title', 'subtitle', 'status', 'num_teams',
            'created_at', 'updated_at'
        } <= contests[0].keys()
        assert contests[0]['num_teams'] == 3
        # assert contests[0]['num_submissions'] == 15

    new_contest = dict(
        title="New Contest",
        subtitle="new contest subtitle",
        description="test desc",
    )

    with request.post('/contests', data=new_contest) as contest:
        assert new_contest.items() <= contest.items()
        assert contest['id'] == 5

    with request.patch('/contests/5', data={'description': 'xxx'}, expected_status_code=202) as contest:
        assert contest['description'] == 'xxx'

    with request.delete('/contests/5', expected_status_code=204):
        with request.get('/contests') as contests:
            assert len(contests) == 4
