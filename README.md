# AWS ALB Status Check
This simple script checks the status of a target instance within an AWS Application Load Balancer (ALB) target group,
and is designed to be run as part of a zero-downtime deployment process. The basic flow would be:
1. Instruct the application to start draining connections
2. Use this script to periodically poll the ALB and wait for the target instance to be marked as unhealthy
3. Once the target instance is unhealthy, proceed with the deployment

The exit code of the script is used to determine the status of the target instance:
- `0`: The target instance is healthy
- `1`: The target instance is unhealthy
- `2`: Other status or error occurred

## Running

### Detect Health
Exit code determines the health of the target instance
```bash
docker run --rm \
    --env "AWS_REGION={region}" \
    --env "AWS_ACCESS_KEY_ID={access_key}" \
    --env "AWS_SECRET_ACCESS_KEY={secret_key}" \
    ghcr.io/rpungello/aws-alb-status:latest "{target_group_arn}" "{ec2_instance_id}"
```

### Wait for Healthy
Block until the target instance is marked as healthy, or until the timeout is reached (default 5 minutes).
```bash
docker run --rm \
    --env "AWS_REGION={region}" \
    --env "AWS_ACCESS_KEY_ID={access_key}" \
    --env "AWS_SECRET_ACCESS_KEY={secret_key}" \
    ghcr.io/rpungello/aws-alb-status:latest --wait-for-healthy "{target_group_arn}" "{ec2_instance_id}"
```

### Wait for Unhealthy
Block until the target instance is marked as unhealthy, or until the timeout is reached (default 5 minutes).
```bash
docker run --rm \
    --env "AWS_REGION={region}" \
    --env "AWS_ACCESS_KEY_ID={access_key}" \
    --env "AWS_SECRET_ACCESS_KEY={secret_key}" \
    ghcr.io/rpungello/aws-alb-status:latest --wait-for-unhealthy "{target_group_arn}" "{ec2_instance_id}"
```

If run from within an EC2 instance running Amazon Linux, you can use the `ec2-metadata` command to retrieve the instance ID automatically:
`ghcr.io/rpungello/aws-alb-status:latest "{target_group_arn}" "$(ec2-metadata --quiet --instance-id)"`
