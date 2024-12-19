import boto3
from config import AWS_ACCESS_KEY_ID,AWS_REGION,AWS_SECRET_ACCESS_KEY,SNS_TOPIC_ARN
# AWS SNS 설정
sns_client = boto3.client(
    "sns",
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = AWS_REGION
)

def send_sns_alert(message):
    """AWS SNS를 통해 알림을 전송합니다."""
    try:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message
        )
        print(f"Alert sent! Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send alert: {e}")
