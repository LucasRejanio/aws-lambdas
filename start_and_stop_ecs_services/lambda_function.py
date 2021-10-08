import json
import boto3

ASSUMED_ROLE = {
       "ci": "arn:aws:iam::427765223009:role/CIAccountAccessRole",
       "staging": "arn:aws:iam::033687817760:role/StagingAccountAccessRole"
    }

def load_policy_from_json(name):
    with open(f"{name}.json", 'r') as rule:
        data = rule.read()
    return json.loads(data)

def get_ip(task):
    details = task['attachments'][0]['details']
    for detail in details:
        if detail['name'] == "networkInterfaceId":
            interface = detail['value']
    ec2 = boto3.resource('ec2')
    network_interface = ec2.NetworkInterface(interface)
    return network_interface.association_attribute['PublicIp']

def rule_ecs(policy):
    if 'ecs_assume_role' in policy:
        sts_client = boto3.client('sts')
        destination_account_role = sts_client.assume_role(
            RoleArn=ASSUMED_ROLE[policy['ecs_assume_role']],
            RoleSessionName="cross_acct_lambda"
        )
        ecs_client = boto3.client(
            'ecs',
            aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
            aws_session_token=destination_account_role['Credentials']['SessionToken'],
            region_name=policy['region']
        )
    else:
        ecs_client = boto3.client('ecs')
    ecs_client.update_service(
        cluster=policy['cluster'],
        service=policy['service'],
        desiredCount=policy['desired_count']
    )

def rule_rds(policy):
    if 'rds_assume_role' in policy:
        sts_client = boto3.client('sts')
        destination_account_role = sts_client.assume_role(
            RoleArn=ASSUMED_ROLE[policy['rds_assume_role']],
            RoleSessionName="cross_acct_lambda"
        )
        rds_client = boto3.client(
            'rds',
            aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
            aws_session_token=destination_account_role['Credentials']['SessionToken'],
            region_name=policy['region']
        )
    else:
        rds_client = boto3.client('rds')

    status = rds_client.describe_db_clusters(
        DBClusterIdentifier=policy['cluster']
    )['DBClusters'][0]['Status']

    if policy['action'] == "start":
        if status == "stopped":
            rds_client.start_db_cluster(
                DBClusterIdentifier=policy['cluster']
            )
    elif policy['action'] == "stop":
        if status == "available":
            rds_client.stop_db_cluster(
                DBClusterIdentifier=policy['cluster']
            )

def rule_sqs(policy):
    if 'sqs_assume_role' in policy:
        sts_client = boto3.client('sts')
        destination_account_role = sts_client.assume_role(
            RoleArn=ASSUMED_ROLE[policy['sqs_assume_role']],
            RoleSessionName="cross_acct_lambda"
        )
        sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
            aws_session_token=destination_account_role['Credentials']['SessionToken'],
            region_name=policy['region']
        )
    else:
        sqs_client = boto3.client('sqs')
    sqs_client.purge_queue(
        QueueUrl=policy['queue_url']
    )

def rule_lambda(policy):
    if 'lambda_assume_role' in policy:
        sts_client = boto3.client('sts')
        destination_account_role = sts_client.assume_role(
            RoleArn=ASSUMED_ROLE[policy['lambda_assume_role']],
            RoleSessionName="cross_acct_lambda"
        )
        lambda_client = boto3.client(
            'lambda',
            aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
            aws_session_token=destination_account_role['Credentials']['SessionToken'],
            region_name=policy['region']
        )
    else:
        lambda_client = boto3.client('lambda')
    lambda_client.update_event_source_mapping(
        UUID=policy['uuid'],
        FunctionName=policy['function_name'],
        Enabled=policy['enabled']
    )

def rule_route53(policy):
    if 'ecs_assume_role' in policy:
        sts_client = boto3.client('sts')
        destination_account_role = sts_client.assume_role(
            RoleArn=ASSUMED_ROLE[policy['ecs_assume_role']],
            RoleSessionName="cross_acct_lambda"
        )
        ecs_client = boto3.client(
            'ecs',
            aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
            aws_session_token=destination_account_role['Credentials']['SessionToken'],
            region_name=policy['region']
        )
    else:
        ecs_client = boto3.client('ecs')

    task_list = ecs_client.list_tasks(
        cluster=policy['cluster'],
        serviceName=policy['service'],
        desiredStatus='RUNNING',
    )
    tasks = ecs_client.describe_tasks(
        cluster=policy['cluster'],
        tasks=task_list['taskArns'],
    )
    for task in tasks['tasks']:
        task_ip = get_ip(task)
        if 'route53_assume_role' in policy:
            sts_client = boto3.client('sts')
            destination_account_role = sts_client.assume_role(
                RoleArn=ASSUMED_ROLE[policy['route53_assume_role']],
                RoleSessionName="cross_acct_lambda"
            )
            route53_client = boto3.client(
                'route53',
                aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
                aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
                aws_session_token=destination_account_role['Credentials']['SessionToken'],
                region_name=policy['region']
            )
        else:
            route53_client = boto3.client('route53')

        route53_client.change_resource_record_sets(
            HostedZoneId=policy['zone'],
            ChangeBatch={
                'Comment': 'string',
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': policy['record'],
                            'Type': 'A',
                            'TTL': 60,
                            'ResourceRecords': [
                                    {
                                        'Value': task_ip
                                    },
                            ]
                        }
                    }
                ]
            }
        )

def rule_security_group_ingress(policy):
    if 'ecs_assume_role' in policy:
        sts_client = boto3.client('sts')
        destination_account_role = sts_client.assume_role(
            RoleArn=ASSUMED_ROLE[policy['ecs_assume_role']],
            RoleSessionName="cross_acct_lambda"
        )
        ecs_client = boto3.client(
            'ecs',
            aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
            aws_session_token=destination_account_role['Credentials']['SessionToken'],
            region_name=policy['region']
        )
    else:
        ecs_client = boto3.client('ecs')

    task_list = ecs_client.list_tasks(
        cluster=policy['cluster'],
        serviceName=policy['service'],
        desiredStatus='RUNNING',
    )
    tasks = ecs_client.describe_tasks(
        cluster=policy['cluster'],
        tasks=task_list['taskArns'],
    )
    for task in tasks['tasks']:
        task_ip = get_ip(task)
        ip_cidr = task_ip + '/32'
        if 'ec2_assume_role' in policy:
            sts_client = boto3.client('sts')
            destination_account_role = sts_client.assume_role(
                RoleArn=ASSUMED_ROLE[policy['ec2_assume_role']],
                RoleSessionName="cross_acct_lambda"
            )
            ec2_client = boto3.resource(
                'ec2',
                aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
                aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
                aws_session_token=destination_account_role['Credentials']['SessionToken'],
                region_name=policy['region']
            )
        else:
            ec2_client = boto3.resource('ec2')

        security_group = ec2_client.SecurityGroup(
            policy['security_group'])
        security_group.authorize_ingress(
            CidrIp=ip_cidr,
            FromPort=policy['port'],
            IpProtocol=policy['protocol'],
            ToPort=policy['port']
        )

def rule_event(policy):
    if 'event_assume_role' in policy:
        sts_client = boto3.client('sts')
        destination_account_role = sts_client.assume_role(
            RoleArn=ASSUMED_ROLE[policy['event_assume_role']],
            RoleSessionName="cross_acct_lambda"
        )
        events_client = boto3.client(
            'events',
            aws_access_key_id=destination_account_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=destination_account_role['Credentials']['SecretAccessKey'],
            aws_session_token=destination_account_role['Credentials']['SessionToken'],
            region_name=policy['region']
        )
    else:
        events_client = boto3.client('events')

    if policy['enabled'] == True:
        events_client.enable_rule(
            Name=policy['rule_name']
        )
    elif policy['enabled'] == False:
        events_client.disable_rule(
            Name=policy['rule_name']
        )


def lambda_handler(event, context):
    policies = load_policy_from_json(event['file'])
    for policy in policies:
        if policy['type'] == "ecs":
            rule_ecs(policy)
        elif policy['type'] == "rds":
            rule_rds(policy)
        elif policy['type'] == "sqs":
            rule_sqs(policy)
        elif policy['type'] == "lambda":
            rule_lambda(policy)
        elif policy['type'] == "route53":
            rule_route53(policy)
        elif policy['type'] == "event":
            rule_event(policy)
        elif policy['type'] == "security_group_ingress":
            rule_security_group_ingress(policy)
