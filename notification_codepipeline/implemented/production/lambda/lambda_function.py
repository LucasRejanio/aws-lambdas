import requests
import json
import datetime, pytz
import boto3


def lambda_handler(event, context):
    message_str = event['Records'][0]['Sns']['Message']
    message = json.loads(message_str)

    pipeline = message['detail']['pipeline']
    state = message['detail']['state']
    stage = message['detail']['stage']

    actions = []

    if state == "STARTED" and stage == "Source":
        state_pipeline = "Start Deploy of "
        title = state_pipeline + pipeline
        color = "36C5F0"
    elif state == "SUCCEEDED" and stage == "Build":
        state_pipeline = "Finish Deploy of "
        title = state_pipeline + pipeline
        color = "2EB67D"
    elif state == "FAILED":
        state_pipeline = "There was an error in the Deploy of "
        documentation = "See the documentation for troubleshooting"
        note = "NOTE: To view the logs you need to be logged in the QA role"
        title = state_pipeline + pipeline + "\n" + documentation + "\n" + note
        color = "E01E5A"
        
        actions = [
            {
                "type": "button",
                "text": "Open Log Error",
                "style": "danger",
                "url": f"https://console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline}/view?region=us-east-1"
            },
            {
                "type": "button",
                "text": "Documentation",
                "url": "https://enjoei.atlassian.net/wiki/spaces/INF/pages/383845948/Deploy+CodePipeline"
            }
        ]
    else:
        return 0
    
    tz_america_sp = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    time_now = tz_america_sp.strftime("%d-%m-%Y: %H:%M:%S")

    payload_dict = {
        "attachments": [
            {
                "title": title,
                "text": "at " + time_now,
                "color": color,
                "actions": actions
            }
        ]
    }

    payload = str(payload_dict)

    client_ssm = boto3.client('ssm')

    parameters = client_ssm.get_parameter(
        Name='/notification/production/lambda/slack_urls',
        WithDecryption=True
    )

    urls_str = parameters['Parameter']['Value']
    urls = json.loads(urls_str)
    url = urls["production"]

    requests.request("POST", url, data=payload)
