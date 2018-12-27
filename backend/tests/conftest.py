from datetime import datetime
import pytest
from pony.orm import db_session

from aivivn_backend.app import app
from aivivn_backend.models import db, Contest, Participation, User, Submission


def reset_database(db):
    db.drop_all_tables(with_all_data=True)
    db.create_tables()


@db_session
def populate_database():
    if not User.select().exists():
        u1 = User(username='user1', email='user1@example.com', password='password')
        u2 = User(username='user2', email='user2@example.com', password='password')
        u3 = User(username='user3', email='user3@example.com', password='password')
        u4 = User(username='user4', email='user4@example.com', password='password')
        u5 = User(username='user5', email='user5@example.com', password='password')
        u6 = User(username='user6', email='user6@example.com', password='password')

    if not Contest.select().exists():
        c1 = Contest(title='Contest 1', subtitle="Subtitle 1", description='Contest 1 Description')
        c2 = Contest(title='Contest 2', description='Contest 2 Description')
        Contest(title='Contest 3', description='Contest 3 Description')
        Contest(title='Contest 4', description='Contest 4 Description')

        Participation(contest=c2, user=u1, team_name="team1", last_week_rank=2)
        Participation(contest=c2, user=u2, team_name="team2", last_week_rank=2)
        Participation(contest=c2, user=u3, team_name="team3", last_week_rank=2)

        p1 = Participation(contest=c1, user=u1, team_name="team1", last_week_rank=2)
        p2 = Participation(contest=c1, user=u2, team_leader=p1)
        p3 = Participation(contest=c1, user=u3, team_leader=p1)
        p4 = Participation(contest=c1, user=u4, team_name="team2", last_week_rank=1)
        p5 = Participation(contest=c1, user=u5, team_leader=p4)
        p6 = Participation(contest=c1, user=u6, team_name="team3", last_week_rank=3)

        Submission(participation=p1, public_score=70.5, created_at=datetime.utcnow())
        Submission(participation=p1, public_score=89.4, created_at=datetime.utcnow())
        Submission(participation=p2, public_score=90.0, created_at=datetime.utcnow())
        Submission(participation=p3, public_score=50.4, created_at=datetime.utcnow())
        Submission(participation=p3, public_score=60.5, created_at=datetime.utcnow())
        Submission(participation=p3, public_score=80.7, created_at=datetime.utcnow())
        Submission(participation=p3, public_score=55.4, created_at=datetime.utcnow())

        Submission(participation=p4, public_score=10.0, created_at=datetime.utcnow())
        Submission(participation=p4, public_score=10.5, created_at=datetime.utcnow())
        Submission(participation=p5, public_score=20.0, created_at=datetime.utcnow())
        Submission(participation=p5, public_score=10.0,  created_at=datetime.utcnow())
        Submission(participation=p5, public_score=100.0,  created_at=datetime.utcnow())

        Submission(participation=p6, public_score=30.0,  created_at=datetime.utcnow())
        Submission(participation=p6, public_score=31.0,  created_at=datetime.utcnow())
        Submission(participation=p6, public_score=30.2,  created_at=datetime.utcnow())


@pytest.fixture(autouse=True)
def client():
    client = app.test_client()

    populate_database()

    pytest.is_dirty = False

    yield client

    if pytest.is_dirty:
        reset_database(db)
