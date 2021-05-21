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

    if state == "STARTED" and stage == "Source":
        state_pipeline = "Start Deploy of "
        color = "36C5F0"
    elif state == "SUCCEEDED" and stage == "Build":
        state_pipeline = "Finish Deploy of "
        color = "2EB67D"
    elif state == "FAILED":
        state_pipeline = "There was an error in the Deploy of "
        color = "E01E5A"
    else:
        return 0
    
    tz_america_sp = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    time_now = tz_america_sp.strftime("%d-%m-%Y: %H:%M:%S")

    payload_dict = {
        "attachments": [
            {
                "title": state_pipeline + pipeline,
                "text": "at " + time_now,
                "color": color
            }
        ]
    }

    payload = str(payload_dict)

    client_ssm = boto3.client('ssm')

    parameters = client_ssm.get_parameter(
        Name='/notifications/production/slack_urls',
        WithDecryption=True
    )

    urls_str = parameters['Parameter']['Value']
    urls = json.loads(urls_str)

    for key in urls.keys():
        if pipeline.__contains__(key):
            url = urls[key]
            requests.request("POST", url, data=payload)
