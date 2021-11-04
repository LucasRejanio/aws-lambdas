import requests
import json
import datetime, pytz
import boto3


def lambda_handler(event, context):
    ## Get message in the event
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # Get infos of message
    pipeline = message['detail']['pipeline']
    state = message['detail']['state']
    stage = message['detail']['stage']

    ## Set actions to null
    actions = []

    ## Validadtion of state deploy
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
        
        ## Creating buttons to slack request
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
    
    ## Formating timezone
    tz_america_sp = datetime.datetime.now(tz=pytz.timezone('America/Sao_Paulo'))
    time_now = tz_america_sp.strftime("%d-%m-%Y: %H:%M:%S")

    ## Payload to request
    payload = str({
        "attachments": [
            {
                "title": title,
                "text": "at " + time_now,
                "color": color,
                "actions": actions
            }
        ]
    })

    ## Get paramet with slack webhooks
    client_ssm = boto3.client('ssm')
    parameters = client_ssm.get_parameter(
        Name='/notification/staging/lambda/slack_urls',
        WithDecryption=True
    )

    ## Get value of parameter
    urls = json.loads(parameters['Parameter']['Value'])

    ## Post message in the slack
    for key in urls.keys():
        if pipeline.__contains__(key):
            url = urls[key]
            requests.request("POST", url, data=payload)
