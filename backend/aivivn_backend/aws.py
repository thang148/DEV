import boto3
from datetime import timedelta
import os


# AWS_ACCESS_KEY_ID = 'ACCESS_KEY_ID'
# AWS_SECRET_ACCESS_KEY = 'SECRET_ACCESS_KEY'

# Submission File
SUBMISSION_UPLOAD_BUCKET = os.getenv('SUBMISSION_UPLOAD_BUCKET', 'default-bucket')

SUBMISSION_FILE_ACL = 'authenticated-read'
SUBMISSION_URL_EXPIRE = timedelta(minutes=10).total_seconds()


def create_submission_key(contest_id, participation_id, submission_id):
    return f'submissions/{contest_id}/{participation_id}/{submission_id}'


def extract_submission_ids(key):
    return [
        int(_id) for _id in key.split('/')[-3:]
    ]


def create_contest_label_key(contest_id, public=True):
    if public:
        return f'contests/{contest_id}/public'
    return f'contests/{contest_id}/private'


def create_submission_presigned_post(contest_id, participation_id, submission_id):
    client = boto3.client('s3')
    bucket = SUBMISSION_UPLOAD_BUCKET
    key = create_submission_key(contest_id, participation_id, submission_id)

    return client.generate_presigned_post(
        Bucket=bucket,
        Key=key,
        Fields={'acl': SUBMISSION_FILE_ACL},
        Conditions=[{'acl': SUBMISSION_FILE_ACL}],
        ExpiresIn=SUBMISSION_URL_EXPIRE
    )
