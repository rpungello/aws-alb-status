#!/usr/bin/env bash
# Usage: drain.sh <target-group-arn>

for i in in $(seq 1 60);
do
	docker run --rm --env "AWS_REGION={region}" --env "AWS_ACCESS_KEY_ID={access_key}" --env "AWS_SECRET_ACCESS_KEY={secret_key}" ghcr.io/rpungello/aws-alb-status:latest $1 "$(ec2-metadata --quiet --instance-id)" &>/dev/null
	if [ "$?" == "1" ]; then
		exit 0
	else
		echo "Waiting for load balancer"
	fi

	sleep 5
done

echo "Timeout exceeded"
exit 1