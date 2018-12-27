from .abstract import ScoreError


class HeaderError(ScoreError):
    """Raised when the header of submission is not correct"""
    pass


class NumRowError(ScoreError):
    """Raised when the number of row of submission is not correct"""
    pass


class PredictValueError(ScoreError):
    """Raised when the label value of submission is not correct"""
    pass


class IdTestCaseError(ScoreError):
    """Raised when the test case of submission is not correct"""
    pass


class UnknownEvaluatorError(ScoreError):
    """Raised when the test case of submission is not correct"""
    pass
