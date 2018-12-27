import csv
from abc import ABC


class DataFrame(ABC):
    def __init__(
        self,
        csv_file,
        label,
        label_type,
        id
    ):
        self.csv_file = csv_file
        self.label = label
        self.label_type = label_type
        self.id = id

        # Get dicts of csv
        self.headers, self.csv_dict = self._get_dict_csv(self.csv_file, self.label_type)
        self.num_rows = len(self.csv_dict)

        # Sort the csv_dict
        self.csv_dict = dict(sorted(self.csv_dict.items()))
        # label_values
        self.label_values = list(self.csv_dict.values())
        # test cases
        self.test_cases = list(self.csv_dict.keys())

    def _get_dict_csv(self, csv_file, mytype=float):
        """
        :param fn_csv: a str, path to csv file, suppose this csv has only two columns: id and label
                mytype: type of label
        :return: a dict, key is the id, value is the label
        """
        try:
            res = dict()
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            headers = next(csv_reader)
            for row in csv_reader:
                res[row[0]] = mytype(row[1])
        except Exception as e:
            return [], {}
        else:
            return headers, res
