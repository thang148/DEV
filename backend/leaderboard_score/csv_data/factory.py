from io import StringIO
import boto3

from .data_frame import DataFrame


class DataFrameFactory(object):
    def __init__(
        self,
        label,
        label_type,
        id
    ):
        self.label = label
        self.label_type = label_type
        self.id = id

    def create(self, csv_file):
        return DataFrame(
            csv_file,
            self.label,
            self.label_type,
            self.id
        )

    def create_from_s3(self, bucket, key):
        s3 = boto3.resource('s3')
        obj = s3.Object(bucket, key)
        body = obj.get()['Body'].read().decode('utf-8')
        return DataFrame(
            StringIO(body),
            self.label,
            self.label_type,
            self.id
        )
