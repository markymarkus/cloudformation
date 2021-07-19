## AWS deployment role with Permissions Boundary
Scenario here is, we create a deployment role which can be assumed(ie. used) by cross-account principal(IAM::Role or IAM::User). With Permissions Boundary, we set boundaries which cannot be exceed.

Deployment role allows following actions:
Full access to:
- cloudformation:*
- lambda:*
- logs:*
- s3:*

Limited access to:
- IAM. New roles can be created as long as Permissions Boundary is used. Modifications to Permissions Boundary are not allowed.

In short, this blocks pretty efficiently privilege escalation which is result of granting principal an access to control IAM Role and Policies.  

## Create deployment role
```shell
aws cloudformation deploy --template-file ci-role.yaml --stack-name deploy-role --parameter-overrides TrustedPrincipalArn=arn:aws:iam::999999999999:user/markus --capabilities CAPABILITY_NAMED_IAM

aws cloudformation describe-stacks --stack-name deploy-role --query 'Stacks[*].Outputs[]'
# now we have deployment role arn, let us assume the role, from account 999999999999
source assumerole.sh arn:aws:iam::11111111111111:role/deploy-role-CiRole-F85WQA3W91QI
aws sts get-caller-identity
"Arn": "arn:aws:sts::11111111111111:assumed-role/deploy-role-CiRole-F85WQA3W91QI/sumething"
```

## Test 1: Create and assume an admin role and do something
If Permissions Boundary is not set, this would be a very easy way to get an elevated access to AWS -> "Create a new role with Admin rights and assume the role". Let's test how it goes now:
```shell
aws iam create-role --role-name testing --assume-role-policy-document file://assumepolicy.json 
# AccessDenied, no permissions boundary parameter given
aws iam create-role --role-name testing --assume-role-policy-document file://assumepolicy.json --permissions-boundary arn:aws:iam::11111111111111:policy/ci-permissions-boundary
# Done
aws iam attach-role-policy --role-name testing --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
# Done
source assumerole.sh arn:aws:iam::11111111111111:role/testing
aws sts get-caller-identity
"Arn": "arn:aws:sts::11111111111111:assumed-role/testing/sumething2"
aws rds describe-db-instances
# AccessDenied, even though we are using AdministratorAccess policy, permissions boundary denies rds action
aws lambda list-functions
# Done, Lambda is allowed 
```


## Test 2: Modify permissions boundary
Another common way to get elevated access rights is to modify access policy(in this case Permissions Policy) and just edit in wanted rights.
```shell
source assumerole.sh arn:aws:iam::11111111111111:role/deploy-role-CiRole-F85WQA3W91QI
# Switched back to the original deployment role
aws iam create-policy-version --policy-arn arn:aws:iam::11111111111111:policy/ci-permissions-boundary --policy-document file://allow_all_policy.json
# AccessDenied "ci-permissions-boundary" can't be modified
aws iam put-role-permissions-boundary --role-name deploy-role-CiRole-F85WQA3W91QI --permissions-boundary file://allow_all_policy.json
# Access Denied
aws iam delete-role-permissions-boundary --role-name deploy-role-CiRole-F85WQA3W91QI 
# Access Denied
```