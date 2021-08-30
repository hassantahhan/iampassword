## Overview
Set IAM Password Policy for all your AWS accounts according to AWS Foundational Security Best Practices standard, which states that "password policies for IAM users should have strong configurations".<br/>
https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-iam-7<br/>

Notes:<br/>
- AWS highly recommends as a best practice that instead of creating IAM users to use federation, via AWS SSO.<br/>
- This solution sets the minimum requirements to pass AWS Security Hub checks - set other parameters as required.<br/>
- Consider implemeting a Service Control Policy (SCP) to disallow linked accounts from resetting IAM Password Policies.<br/>

## Environment
The Lambda function has no external dependencies other than Python 3.9 and Boto3, which is the AWS SDK for Python. The Lambda function requires access to action (iam:UpdateAccountPasswordPolicy) to run. The suggested timeout is 10 seconds.<br/>

## Deployment
You can deploy the Lambda function using AWS CloudFormation (check cloudformation.yml file). Also, you can use AWS CloudFormation StackSets to update the password policy across multiple accounts or the entire AWS Organization.<br/>

## Governance
Once the IAM Passowrd Policies across your linked accounts are updated according to your organization standard, you can implement a Service Control Policy (see the example below) to deny further access to the action,  IAM:UpdateAccountPasswordPolicy. Note that Service Control Policies don't affect users or roles in the management account. <br/>
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUpdateAccountPasswordPolicy",
      "Effect": "Deny",
      "Action": "iam:UpdateAccountPasswordPolicy",
      "Resource": "*"
    }
  ]
}
```
## Testing
The core logic (other than the handler method) can be tested locally without the need for Lambda deployment. I provided two files (test.py and requirements.txt) to help you install and run the code locally. You still need to have your AWS access credentials in .aws\credentials for the test script to work. <br/>

If you like to activly monitor your IAM user permissions for the IAM action, UpdateAccountPasswordPolicy, consider using the IAM Canary concept publish earlier on github. <br/> https://github.com/hassantahhan/iamcanary <br/>

## Cost
The total cost of the Lambda function is estimated to be 0 USD/month.
