from __future__ import print_function
import json
import boto3
import urllib3

SUCCESS = 'SUCCESS'
FAILED = 'FAILED'
http = urllib3.PoolManager()

# cfn-response module
def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    responseUrl = event['ResponseURL']
    print('responseUrl: ' + responseUrl)

    responseBody = {
        'Status' : responseStatus,
        'Reason' : reason or "See the details in CloudWatch Log Stream: {}".format(context.log_stream_name),
        'PhysicalResourceId' : physicalResourceId or context.log_stream_name,
        'StackId' : event['StackId'],
        'RequestId' : event['RequestId'],
        'LogicalResourceId' : event['LogicalResourceId'],
        'NoEcho' : noEcho,
        'Data' : responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:")
    print(json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)
    except Exception as e:
        print("send(..) failed executing http.request(..):", e)

# lambda handler for IAM password policy remediator
def lambda_handler(event, context):
    print('lambda_handler() received event: ' + json.dumps(event))
    result = FAILED

    try:
        if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
            response = set_iam_password_policy()
            print('iam password policy update completion response: ' + str(response))
            result = SUCCESS
        elif event['RequestType'] == 'Delete':
            print('deletion of CloudFormation stack has no impact on current password policy')
            result = SUCCESS
    except Exception as e:
        print('lambda_handler error: ' + str(e))
        result = FAILED

    send(event, context, result, {})
    return

# Reset IAM Password Policy for AWS Account according to AWS Foundational Security Best Practices Standard
# https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html#fsbp-iam-7
#
# Notes:
# 1- AWS highly recommends that instead of creating IAM users to you use federation, as a best practice.
# 2- The function sets minimum requirements to pass Security Hub check, change default values as required.
def set_iam_password_policy():
    iam = boto3.client('iam')

    response = iam.update_account_password_policy(
        # change default values as required considering AWS best practice for access federation
        #AllowUsersToChangePassword = False, # default value (users can't change passwords)
        #HardExpiry = False,                 # default value (users can continue to sign-in)
        #MaxPasswordAge = 0,                 # default value (user passwords never expire)
        #PasswordReusePrevention = 0,        # default value (password reuse is allowd)

        # set parameters as required by Security Hub [IAM.7] contor
        RequireNumbers = True,              # must contain at least one numeric character (0 to 9)
        RequireSymbols = True,              # at least one of the characters: ! @ # $ % ^ & * ( ) _ + - = [ ] { } | '
        MinimumPasswordLength = 8,          # 8 is minimum required length by Security Hub IAM.7 contorl
        RequireUppercaseCharacters = True,  # at least one uppercase character from alphabet (A to Z)
        RequireLowercaseCharacters = True,  # at least one lowercase character from alphabet (a to z)
    )

    return 'set_iam_password_policy() completion response: ' + str(response)
