import requests
import json
import datetime, pytz
import boto3
import os


def message_formater(pipeline, state, stage):
    # Seting collor default to button in actions
    style_button = "primary"

    # Validating the deploy state
    if state == "STARTED" and stage == "Source":
        state_pipeline = "Start " + pipeline
        color = "36C5F0"
    elif state == "SUCCEEDED" and stage == "Deploy":
        state_pipeline = "Finish " + pipeline 
        color = "2EB67D"
    elif state == "FAILED":
        state_pipeline = "There was error with " + pipeline
        color = "E01E5A"
        style_button = "danger"
    
    if pipeline.__contains__('lambda'):
        if state == "SUCCEEDED" and stage == "Build":
            state_pipeline = "Finish " + pipeline 
            color = "2EB67D"
    
    # Formating timezone
    tz_america_sp = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    time_now = tz_america_sp.strftime("%d-%m-%Y: %H:%M:%S")
    
    # Payload to request
    payload = str({
        "attachments": [
            {
                "title": state_pipeline,
                "text": "at " + time_now,
                "color": color,
                "actions": [
                    {
                        "type": "button",
                        "text": "Pipeline",
                        "style": style_button,
                        "url": f"https://console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline}/view?region=us-east-1"
                    },
                    {
                        "type": "button",
                        "text": "Documentation",
                        "url": "https://enjoei.atlassian.net/wiki/spaces/INF/pages/383845948/Deploy+CodePipeline"
                    }
                ]
            }
        ]
    })

    return payload


def slack_messenger(pipeline, payload):
    # Getting local env and parameter store with slack webhooks
    environment = os.environ['ENVIRONMENT']

    client_ssm = boto3.client('ssm')
    parameters = client_ssm.get_parameter(
        Name=f'/notification/{environment}/service/slack_urls',
        WithDecryption=True
    )
    urls = json.loads(parameters['Parameter']['Value'])

    # Sending message to slack 
    places = ["0", "mercury", "venus", "earth", "mars", "next"]
    for place in places:
        if pipeline.__contains__(place):
            for key in urls.keys():
                if pipeline.__contains__(key):
                    url = urls[key]
    
    if not place in places:
        url = urls[environment]
    
    requests.request("POST", url, data=payload)


def lambda_handler(event, context):
    # Getting message in the event
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # Getting attributes of message
    pipeline = message['detail']['pipeline']
    state = message['detail']['state']
    stage = message['detail']['stage']

    # Calling functions
    payload = message_formater(pipeline, state, stage)
    slack_messenger(pipeline, payload)
