from pony.orm import db_session

from aivivn_backend.app import db  # noqa
from aivivn_backend.models import Contest, Submission
from aivivn_backend.aws import extract_submission_ids
from leaderboard_score import LeaderBoardScore, DataFrameFactory
from leaderboard_score.error import ScoreError


@db_session
def score_submission(event, context):
    """
    {
    "Records":[
        {
            "eventVersion":"2.0",
            "eventSource":"aws:s3",
            "awsRegion":"us-east-1",
            "eventTime":The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z
            "eventName":"event-type",
            "userIdentity":{
                "principalId":"Amazon-customer-ID-of-the-user-who-caused-the-event"
            },
            "requestParameters":{
                "sourceIPAddress":"ip-address-where-request-came-from"
            },
            "responseElements":{
                "x-amz-request-id":"Amazon S3 generated request ID",
                "x-amz-id-2":"Amazon S3 host that processed the request"
            },
            "s3":{
                "s3SchemaVersion":"1.0",
                "configurationId":"ID found in the bucket notification configuration",
                "bucket":{
                "name":"bucket-name",
                "ownerIdentity":{
                    "principalId":"Amazon-customer-ID-of-the-bucket-owner"
                },
                "arn":"bucket-ARN"
                },
                "object":{
                "key":"object-key",
                "size":object-size,
                "eTag":"object eTag",
                "versionId":"object version if bucket is versioning-enabled, otherwise null",
                "sequencer": "a string representation of a hexadecimal value used to determine event sequence,
                    only used with PUTs and DELETEs"
                }
            }
        },
    ]
    }
    """
    object_key = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    contest_id, participation_id, submission_id = extract_submission_ids(object_key)

    submission = Submission[submission_id]
    contest = Contest[contest_id]

    meta = contest.scoring_meta
    df_factory = DataFrameFactory(
        label=meta['label'],
        label_type=meta['label_type'],
        id=meta['id']
    )

    leader_board_score = LeaderBoardScore(
        public_gt=df_factory.create_from_s3(bucket_name, meta['public']),
        private_gt=df_factory.create_from_s3(bucket_name, meta['private']),
        label=meta['label'],
        id=meta['id'],
        evaluator_name=meta['evaluator_name']
    )

    submission_df = df_factory.create_from_s3(bucket_name, object_key)
    try:
        leader_board_score.check_submission(submission_df)
        submission.private_score = leader_board_score.evaluate_private_score(submission_df)
        submission.public_score = leader_board_score.evaluate_public_score(submission_df)
    except ScoreError as e:
        submission.comment = e.comment
    else:
        submission.comment = 'ok'
