# Github OIDC role

1. Update `GithubRepoName` parameter and deploy github-oidc.yml
2. Configure to Github settings IAM role ARN.
3. Configure to /workflows/
```
- uses: aws-actions/configure-aws-credentials@v1
with:
    role-to-assume: ${{ secrets.GITHUB_IAMROLE_ARN }}
    role-session-name: gh-actions-session
    aws-region: ${{ secrets.AWS_REGION }}
```