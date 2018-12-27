import pytest
from sklearn.metrics import mean_squared_error

from ..error import UnknownEvaluatorError
from ..score import LeaderBoardScore
from ..csv_data import DataFrameFactory

# Label and ID
df_factory = DataFrameFactory(
    label="label",
    label_type=float,
    id="filename",
)

# Private and public csv files
private_gt_csv = "./leaderboard_score/test/mse_csv/private_true.csv"
public_gt_csv = "./leaderboard_score/test/mse_csv/public_true.csv"

private_gt = df_factory.create(open(private_gt_csv))

public_gt = df_factory.create(open(public_gt_csv))


# Evaluator using is
DEFAULT_EVALUATOR_NAME = "MSEEvaluator"

# Sample submission

# Expect 0.66 public, 0.33 private
sub1 = "./leaderboard_score/test/mse_csv/team1/submission1.csv"
sub1 = df_factory.create(open(sub1))


def get_leaderboard_score(evaluator_name=DEFAULT_EVALUATOR_NAME):
    return LeaderBoardScore(
        public_gt=public_gt,
        private_gt=private_gt,
        id=df_factory.id,
        label=df_factory.label,
        evaluator_name=evaluator_name
    )


def test_leaderboard_score_init_error():
    evaluator_name = "DummyEvaluator"
    with pytest.raises(UnknownEvaluatorError):
        get_leaderboard_score(evaluator_name)


def test_mse_public_score():
    leaderboard_score = get_leaderboard_score()
    sub = sub1
    score = leaderboard_score.evaluate_public_score(sub)
    sk_score = mean_squared_error([0.75, 2.5, 5.0], [0.7, 2.35, 5.09])
    assert round(score, 10) == round(sk_score, 10)


def test_mse_private_score():
    leaderboard_score = get_leaderboard_score()
    sub = sub1
    score = leaderboard_score.evaluate_private_score(sub)
    sk_score = mean_squared_error([0.5, 1.5], [6.2, 1.0])
    assert round(score, 10) == round(sk_score, 10)
