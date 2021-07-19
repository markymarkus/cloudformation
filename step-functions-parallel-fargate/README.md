# Step Functions with parallel Fargate tasks

Launches parallel Fargate tasks(three with the test data). 
Python X-Ray enabled on created Docker image.

## Deploy
1. Create ECR repository
```
aws cloudformation deploy --template-file cfn/ecr.yaml --stack-name ecr --capabilities CAPABILITY_IAM
```

2. Create Docker image and push to ECR
```
# Get repository URI from the created ECR stack:
export REPOURI=$(aws cloudformation describe-stacks --stack-name ecr --query "Stacks[0].Outputs[?OutputKey=='Uri'].OutputValue" --output text)

# Login
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.eu-west-1.amazonaws.com

# Build with Apple M1 chip:
cd docker
docker buildx build --platform linux/amd64 -t $REPOURI --push .
cd ..
```

3. Create Fargate and Step Functions - resources
Replace SUBNET_ID with your VPC's subnet id to launch Fargate tasks to.
```
aws cloudformation deploy --template-file cfn/stepfunctions-fargate.yaml --stack-name stepfunctions-fargate --parameter-overrides Image=$REPOURI FargateSubnet=SUBNET_ID --capabilities CAPABILITY_NAMED_IAM
```

## Test
```
aws stepfunctions start-execution --state-machine-arn arn:aws:states:eu-west-1:838608195734:stateMachine:StateMachine-8hJt11TgwmU2 --input file://test_input.json
```
