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

    parameter = pipeline.split("-")
    service = parameter[1]
    
    if pipeline.__contains__("0"):
        environment = parameter[2] + "-" + parameter[3]
    else:
        environment = parameter[2]

    if state == "STARTED" and stage == "Source":
        state_pipeline = "Start Deploy of "
        title = state_pipeline + service
        color = "36C5F0"
    elif state == "SUCCEEDED" and stage == "Deploy":
        state_pipeline = "Finish Deploy of "
        title = state_pipeline + service
        color = "2EB67D"
    elif state == "FAILED":
        state_pipeline = "There was an error in the Deploy of "
        documentation = "See the documentation for troubleshooting"
        note = "NOTE: To view the logs you need to be logged in the QA role"
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

        if stage == "Deploy" and service == "website":
            state_pipeline = "There was an error of aplication in the Deploy of "
            action = {
                "type": "button",
                "text": "Datadog",
                "url": f"https://app.datadoghq.com/logs?query=task_family%3A{environment}-{service}-deploy&index="
            },
            actions = actions.append(action)

        title = state_pipeline + service + "\n" + documentation + "\n" + note
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
        Name='/notification/staging/service/slack_urls',
        WithDecryption=True
    )

    urls_str = parameters['Parameter']['Value']
    urls = json.loads(urls_str)

    if pipeline.__contains__("0") or pipeline.__contains__("next"):
        for key in urls.keys():
            if pipeline.__contains__(key):
                url = urls[key]
                requests.request("POST", url, data=payload)
    else:
        url = urls["staging"]
        requests.request("POST", url, data=payload)