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

parser = argparse.ArgumentParser(
    prog='docker run [...]',
    description='A script to interact with AWS ALB and check target health.'
)
parser.add_argument('arn', type=str, help='ARN of the target group to check health for')
parser.add_argument('target', type=str, help='ID of the target instance to check health for')
args = parser.parse_args()

client = get_alb_client()
health = client.describe_target_health(
    TargetGroupArn=args.arn,
    Targets=[
        {
            'Id': args.target
        }
    ]
)

if 'TargetHealthDescriptions' in health and len(health['TargetHealthDescriptions']) > 0:
    target_health = health['TargetHealthDescriptions'][0]['TargetHealth']
    if 'State' in target_health:
        if target_health['State'].lower() == 'healthy':
            print('Target healthy')
        elif target_health['State'].lower() == 'unhealthy':
            print('Target unhealthy')
            exit(1)
        else:
            print(f"Target health state: {target_health['State']}")
            exit(2)
    else:
        print("Target health state not found.")
        exit(2)

else:
    print("No health information found for the specified target.")
    exit(2)