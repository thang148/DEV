from ..csv_data import DataFrameFactory
import pytest

from ..error import (
    HeaderError, NumRowError, IdTestCaseError,
    UnknownEvaluatorError
)
from ..score import LeaderBoardScore

# Label and ID
df_factory = DataFrameFactory(
    label="label",
    label_type=int,
    id="filename",
)

# Private and public csv files
private_gt_csv = "./leaderboard_score/test/acc_csv/private_true.csv"
private_gt = df_factory.create(open(private_gt_csv))

public_gt_csv = "./leaderboard_score/test/acc_csv/public_true.csv"
public_gt = df_factory.create(open(public_gt_csv))


# Evaluator using is
DEFAULT_EVALUATOR_NAME = "AccuracyEvaluator"

# Sample submission

# Expect 0.66 public, 0.33 private
sub1 = "./leaderboard_score/test/acc_csv/team1/submission1.csv"
sub1 = df_factory.create(open(sub1))

# Wrong header format. Expected error code: HEADER_ERROR (1)
sub2 = "./leaderboard_score/test/acc_csv/team1/submission2.csv"
sub2 = df_factory.create(open(sub2))

# Filename of test set error. Expected error code: FILENAME_ERROR (5)
sub3 = "./leaderboard_score/test/acc_csv/team2/submission3.csv"
sub3 = df_factory.create(open(sub3))

# Number of row in test set error. Expected error code: NUM_ROW_ERROR (2)
sub4 = "./leaderboard_score/test/acc_csv/team2/submission4.csv"
sub4 = df_factory.create(open(sub4))

# The value of label in test set is error. Expected error code: LABEL_VALUES_ERROR (4)
sub5 = "./leaderboard_score/test/acc_csv/team3/submission5.csv"
sub5 = df_factory.create(open(sub5))


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


def test_header_error():
    leaderboard_score = get_leaderboard_score()
    sub = sub2
    with pytest.raises(HeaderError):
        leaderboard_score.evaluate_public_score(sub)


def test_numrow_error():
    leaderboard_score = get_leaderboard_score()
    sub = sub4
    with pytest.raises(NumRowError):
        leaderboard_score.evaluate_public_score(sub)

#
# def test_predict_value_error():
#     leaderboard_score = get_leaderboard_score()
#     sub = sub5
#     with pytest.raises(PredictValueError):
#         leaderboard_score.evaluate_public_score(sub)


def test_testcase_error():
    leaderboard_score = get_leaderboard_score()
    sub = sub3
    with pytest.raises(IdTestCaseError):
        leaderboard_score.evaluate_public_score(sub)


def test_accuracy_public_score():
    leaderboard_score = get_leaderboard_score()
    sub = sub1
    score = leaderboard_score.evaluate_public_score(sub)
    assert round(score, 10) == round(2/3, 10)


def test_accuracy_private_score():
    leaderboard_score = get_leaderboard_score()
    sub = sub1
    score = leaderboard_score.evaluate_private_score(sub)
    assert round(score, 10) == round(1/3, 10)
