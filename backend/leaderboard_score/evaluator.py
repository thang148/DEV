from . import csv_data
import ml_metrics as metrics

from .abstract import MLMetricEvaluator


class AccuracyEvaluator(MLMetricEvaluator):
    def __init__(
        self,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str,
        label: str
    ):
        super(AccuracyEvaluator, self).__init__(public_gt, private_gt, id, label)
        self.score_function = self.accuracy

    def accuracy(self, actual, predicted):
        return 1.0 - metrics.ce(actual, predicted)


class MSEEvaluator(MLMetricEvaluator):
    def __init__(
        self,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str,
        label: str
    ):
        super(MSEEvaluator, self).__init__(public_gt, private_gt, id, label)
        self.score_function = metrics.mse


class RMSEEvaluator(MLMetricEvaluator):
    def __init__(
        self,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str,
        label: str
    ):
        super(RMSEEvaluator, self).__init__(public_gt, private_gt, id, label)
        self.score_function = metrics.rmse


class ROC_AUC_Evaluator(MLMetricEvaluator):
    def __init__(
        self,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str,
        label: str
    ):
        super(ROC_AUC_Evaluator, self).__init__(public_gt, private_gt, id, label)
        self.score_function = metrics.auc
