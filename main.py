import argparse
import os
import time

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


def wait_for_target_health(client: BaseClient, arn: str, target: str, health: str, tries: int = 5,
                           delay: int = 5) -> bool:
    for i in range(tries):
        current_health = get_target_health(client, arn, target)
        if current_health == health:
            print(f"Target health is now {health}!")
            return True
        else:
            print(f"Current target health is {current_health}, waiting for {health}... (attempt {i + 1}/{tries})")
        time.sleep(delay)

    return False


parser = argparse.ArgumentParser(
    prog='docker run [...]',
    description='A script to interact with AWS ALB and check target health.'
)
parser.add_argument('arn', type=str, help='ARN of the target group to check health for')
parser.add_argument('target', type=str, help='ID of the target instance to check health for')
parser.add_argument('--wait-for-healthy', action='store_true', help='Wait for status to be healthy before exiting')
parser.add_argument('--wait-for-unhealthy', action='store_true', help='Wait for status to be unhealthy before exiting')
args = parser.parse_args()

main_client = get_alb_client()

if args.wait_for_healthy:
    if wait_for_target_health(main_client, args.arn, args.target, 'healthy'):
        print("Success!")
    else:
        print("Failed to reach healthy state.")
        exit(1)
elif args.wait_for_unhealthy:
    if wait_for_target_health(main_client, args.arn, args.target, 'unhealthy'):
        print("Success!")
    else:
        print("Failed to reach unhealthy state.")
        exit(1)
else:
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
