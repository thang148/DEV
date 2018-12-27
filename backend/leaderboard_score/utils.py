# import pandas as pd
from . import csv_data


def sort_dataframe(
    dataframe: csv_data.DataFrame,
    key: str
):
    return dataframe.sort_values(by=key)


def lists_equal(list1, list2):
    return set(list1) == set(list2)
