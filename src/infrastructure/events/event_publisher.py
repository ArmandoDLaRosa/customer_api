import boto3
import json
import os
from botocore.exceptions import ClientError

class EventPublisher:
    def __init__(self, bucket_name, environment="local"):
        self.bucket_name = bucket_name
        self.environment = environment
        self.s3_client = self._initialize_s3_client()

    def _initialize_s3_client(self):
        if self.environment == "local":
            return boto3.client(
                "s3",
                endpoint_url=os.getenv("LOCALSTACK_URL", "http://localhost:4566"),
                aws_access_key_id="test",
                aws_secret_access_key="test",
                region_name="us-east-1",
            )
        else:
            return boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )

    def publish(self, event, key_prefix="events/"):
        if not hasattr(event, "to_dict"):
            raise ValueError("Event must have a `to_dict` method.")

        event_data = event.to_dict()
        event_key = f"{key_prefix}{event.event_type}/{event.timestamp.isoformat()}.json"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=event_key,
                Body=json.dumps(event_data),
                ContentType="application/json",
            )
            print(f"Event published: {event_key}")
        except ClientError as e:
            print(f"Failed to publish event to S3: {e}")
            raise
