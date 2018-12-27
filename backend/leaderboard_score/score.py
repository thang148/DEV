from . import check
from . import csv_data
from .factory import Factory


class LeaderBoardScore(object):
    def __init__(
            self,
            public_gt: csv_data.DataFrame,
            private_gt: csv_data.DataFrame,
            id: str,
            label: str,
            evaluator_name: str):
        """

        :param public_gt: public ground truth csv
        :param private_gt: private ground truth csv
        :param id: ID column name of the csv files
        :param label: label column name of the csv files
        :param evaluator_name: The evaluator name (Accuracy, RMSE,...)
        """
        # Public and private ground truth
        self.id = id
        self.label = label
        self.evaluator_name = evaluator_name

        self.public_gt = public_gt
        self.private_gt = private_gt

        self.submission_checker = check.SubmissionChecker(
            self.public_gt,
            self.private_gt,
            self.id,
            self.label
        )

        self.evaluator = Factory.make_evaluator(
            evaluator_name,
            self.public_gt,
            self.private_gt,
            self.id,
            self.label
        )

    def check_submission(self, submission: csv_data.DataFrame):
        self.submission_checker.check_submission(submission)

    def evaluate_public_score(self, submission: csv_data.DataFrame):
        self.check_submission(submission)
        return self.evaluator.evaluate_public_score(submission)

    def evaluate_private_score(self, submission: csv_data.DataFrame):
        self.check_submission(submission)
        return self.evaluator.evaluate_private_score(submission)
