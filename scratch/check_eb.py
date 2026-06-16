import boto3

eb = boto3.client('elasticbeanstalk', region_name='us-east-1')

envs = eb.describe_environments(environmentNames=['propertism-prod-2026'])
for env in envs['Environments']:
    print(f"Environment: {env['EnvironmentName']}")
    print(f"  Status: {env['Status']}")
    print(f"  Health: {env['Health']}")
    print(f"  CNAME: {env.get('CNAME', 'N/A')}")
    print(f"  Platform: {env.get('SolutionStackName', 'N/A')}")
    print(f"  Endpoint URL: {env.get('EndpointURL', 'N/A')}")

# Check if we can use EB SSH
try:
    # Try to get the instance ID
    resources = eb.describe_environment_resources(EnvironmentName='propertism-prod-2026')
    for inst in resources['EnvironmentResources']['Instances']:
        print(f"\nEC2 Instance: {inst['Id']}")
except Exception as e:
    print(f"\nCould not describe resources: {e}")

# Check if we can use SSM
ssm = boto3.client('ssm', region_name='us-east-1')
try:
    instances = ssm.describe_instance_information()
    for inst in instances.get('InstanceInformationList', []):
        print(f"\nSSM Instance: {inst['InstanceId']} - Ping: {inst.get('PingStatus')}")
    if not instances.get('InstanceInformationList'):
        print("\nNo SSM managed instances found")
except Exception as e:
    print(f"\nSSM error: {e}")
