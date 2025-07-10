import argparse
import os

import boto3
from botocore.client import BaseClient

def get_alb_client() -> BaseClient:
    return boto3.client(
        'elbv2',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )

def get_target_health(client: BaseClient, arn: str, target: str) -> str:
    health = client.describe_target_health(
        TargetGroupArn=arn,
        Targets=[
            {
                'Id': target
            }
        ]
    )

    if 'TargetHealthDescriptions' in health and len(health['TargetHealthDescriptions']) > 0:
        target_health = health['TargetHealthDescriptions'][0]['TargetHealth']
        if 'State' in target_health:
            return target_health['State'].lower()

    return 'unknown'

parser = argparse.ArgumentParser(
    prog='docker run [...]',
    description='A script to interact with AWS ALB and check target health.'
)
parser.add_argument('arn', type=str, help='ARN of the target group to check health for')
parser.add_argument('target', type=str, help='ID of the target instance to check health for')
args = parser.parse_args()

main_client = get_alb_client()
main_health = get_target_health(main_client, args.arn, args.target)
if main_health == 'healthy':
    print('Target health is healthy!')
    exit(0)
elif main_health == 'unhealthy':
    print('Target health is unhealthy!')
    exit(1)
else:
    print(f'Target health is unknown ({main_health})!')
    exit(2)