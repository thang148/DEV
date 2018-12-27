from abc import ABC, abstractmethod
from . import csv_data


class ScoreError(Exception):
    """Base class for other exceptions"""
    @property
    def comment(self):
        return self.__class__.__name__


class ScoreEvaluator(ABC):
    """
    An abstract class of score evaluator.
    For each kind of competition, the way of evaluation is different.
    For example:
    - Evaluate accuracy
    - Evaluate RMSE
    - Evaluate IOU
    """

    def __init__(
        self,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str,
        label: str
    ):
        self.id = id
        self.label = label

        # Sort the values of two ground truth in the case that submission
        # has different order of id.
        self.public_gt = public_gt
        self.private_gt = private_gt

    def get_pair_values(self, submission: csv_data.DataFrame, gt: csv_data.DataFrame):
        test_cases = gt.test_cases
        sub_on_id = [submission.csv_dict[id] for id in test_cases]
        return sub_on_id, gt.label_values

    # TODO: should we need control evaluate public/private functions by flag?
    @abstractmethod
    def evaluate_private_score(self, submission: csv_data.DataFrame):
        pass

    @abstractmethod
    def evaluate_public_score(self, submission: csv_data.DataFrame):
        pass


class MLMetricEvaluator(ScoreEvaluator):
    """
    The evaluator using ml_metrics package
    """
    def __init__(
        self,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str,
        label: str
    ):
        super(MLMetricEvaluator, self).__init__(public_gt, private_gt, id, label)
        self.score_function = None

    def evaluate_private_score(self, submission: csv_data.DataFrame):
        predict_values, gt_values = self.get_pair_values(submission, self.private_gt)
        return self.score_function(gt_values, predict_values)

    def evaluate_public_score(self, submission: csv_data.DataFrame):
        predict_values, gt_values = self.get_pair_values(submission, self.public_gt)
        return self.score_function(gt_values, predict_values)
