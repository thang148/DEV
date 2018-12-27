import numpy as np

from . import csv_data
from . import utils
from . import error


class SubmissionChecker(object):
    def __init__(
        self,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str,
        label: str
    ):
        # Public and private ground truth
        self.public_gt = public_gt
        self.private_gt = private_gt
        self.id = id
        self.label = label

        self.header = [self.id, self.label]

    def check_submission(self, submission: csv_data.DataFrame):
        self.check_header(submission)
        self.check_num_row(submission)
        # self.check_predict_value(submission)
        self.check_test_case(submission)

    def check_header(self, submission: csv_data.DataFrame):
        """
        Check submission has same header as private_gt and public_gt or not
        :param submission:
        :return: True or False
        """
        submission_headers = submission.headers
        if not utils.lists_equal(submission_headers, self.header):
            raise error.HeaderError

    def check_num_row(self, submission: csv_data.DataFrame):
        """
        Check number of row in submission matches with total of private_gt and public_gt or not
        :param submission:
        :return: True or False
        """
        n_rows = submission.num_rows
        n_total = self.public_gt.num_rows + self.private_gt.num_rows
        if n_rows != n_total:
            raise error.NumRowError

    def check_predict_value(self, submission: csv_data.DataFrame):
        # TODO: only applied for accuracy problem, need to generalize
        all_labels = self.public_gt.label_values + \
                     self.private_gt.label_values
        label_unique = np.unique(all_labels).tolist()
        label_predict = np.unique(submission.label_values).tolist()
        for predict in label_predict:
            if predict not in label_unique:
                raise error.PredictValueError

    def check_test_case(self, submission: csv_data.DataFrame):
        """
        Check test case of submission should be equal to the ids of public_gt + ids of private_gt
        :param submission:
        :return:
        """
        all_ids = self.public_gt.test_cases + self.private_gt.test_cases
        submission_ids = submission.test_cases
        if not utils.lists_equal(all_ids, submission_ids):
            raise error.IdTestCaseError

    def is_csv(self, submission):
        pass
