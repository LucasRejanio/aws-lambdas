import boto3

region = 'us-west-1'
instances = ['i-12345cb6de4f78g9h']
ec2 = boto3.client('ec2', region_name=region)


def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))
