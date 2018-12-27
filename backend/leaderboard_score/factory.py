# import pandas as pd

from . import csv_data
from . import error
from . import evaluator

EVALUATOR = {
    **evaluator.__dict__,
}


class Factory(object):
    @staticmethod
    def make_evaluator(
        name: str,
        public_gt: csv_data.DataFrame,
        private_gt: csv_data.DataFrame,
        id: str, label: str
    ):
        try:
            return EVALUATOR[name](public_gt, private_gt, id, label)
        except KeyError:
            raise error.UnknownEvaluatorError
