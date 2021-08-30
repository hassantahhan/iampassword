## Overview
Reset IAM Password Policy for all your AWS accounts according to AWS Foundational Security Best Practices Standard. https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-iam-7

Notes:
1- AWS highly recommends that instead of creating IAM users to you use federation, as a best practice.
2- The function sets minimum requirements to pass Security Hub check, change default values as required.

## Environment
The Lambda function has no external dependencies other than Python 3.9 and Boto3, which is the AWS Python SDK. The Lambda function requires access to action (iam:UpdateAccountPasswordPolicy) to run. The suggested timeout is 10 seconds.<br/>

## Deployment
You can deployed the Lambda function using AWS CloudFormation (check cloudformation.yml file). Also, you can use AWS CloudFormation StackSets to update the password policy across multiple accounts.<br/>

## Testing
The core logic (other than the handler method) can be tested locally without the need for Lambda deployment. I provided two files (test.py and requirements.txt) to help you install and run the code locally. You still need to have your AWS access credentials in .aws\credentials for the test script to work. <br/>

## Cost
The total cost of the Lambda function is estimated to be 0 USD/month.
