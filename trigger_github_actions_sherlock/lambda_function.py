import os
import boto3
import requests
import json

def lambda_handler(event, context):
    ## Get environment variables
    environment = os.environ.get('ENVIRONMENT')
    path = os.environ.get('PATH')

    ## Get parameter token
    client_ssm = boto3.client('ssm')
    parameter_token = client_ssm.get_parameter(
        Name='/github/api_token',
        WithDecryption=True
    )
    token = str(parameter_token['Parameter']['Value'])

    ## Request to trigger
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = json.dumps({
        "ref": "main",
        "inputs": {
            "environment": environment, 
            "path": path
        }
    })

    url = "https://api.github.com/repos/enjoei/sherlock"\
          "/actions/workflows/sherlock.yml/dispatches"

    response = requests.request("POST", url, headers=headers, data=payload)

    ## Get job id
    job_id = event["CodePipeline.job"]["id"]

    ## Notify CodePipeline
    client_codepipeline = boto3.client('codepipeline')
    if response.status_code == 204:
         client_codepipeline.put_job_success_result(
            jobId=job_id
        )
    else:
        client_codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                'type': 'JobFailed',
                'message': 'Unable to trigger Sherlock action',
            }
        )
