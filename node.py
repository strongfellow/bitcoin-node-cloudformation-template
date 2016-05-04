
import argparse
import sys
import uuid

import boto3

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()

    parser.add_argument('--on-failure',
                        default='DO_NOTHING',
                        choices=['DO_NOTHING', 'ROLLBACK', 'DELETE'])
    parser.add_argument('--vpc', default='vpc-599c723d')
    parser.add_argument('--subnet', default='subnet-09ee1e6d')
    parser.add_argument('--key-name', default='thinkpad')
    parser.add_argument('--instance-type',
                        default='m4.large')
    parser.add_argument('--rpc-password',
                        required=False)
    parser.add_argument('--snapshot-id',
                        default='snap-a127e2f3')
    parser.add_argument('--stage',
                        default='prod',
                        choices=['dev', 'test', 'staging', 'prod'])
    parser.add_argument('--mode',
                        default='Webapp',
                        choices=['AWSListener', 'EdgeNode', 'Webapp'])
    parser.add_argument('--nickname', required=True)
    parser.add_argument('--bitcoin-version',
                        default='v0dot12dot1',
                        choices=['v0dot12dot1'])

    args = parser.parse_args(args)

    stack_name = '{nickname}-{mode}-{stage}'.format(
        nickname=args.nickname,
        mode=args.mode,
        stage=args.stage)
    host_nick_name = stack_name
    timeout_in_minutes = 10

    rpc_password = str(uuid.uuid4())

    body = open('baked-node.json').read()

    client = boto3.client('cloudformation')
    response = client.create_stack(
        StackName=stack_name,
        TemplateBody=body,
        Parameters=[
            {
                'ParameterKey': 'VPC',
                'ParameterValue': args.vpc
            },
            {
                'ParameterKey': 'Subnet',
                'ParameterValue': args.subnet
            },
            {
                'ParameterKey': 'KeyName',
                'ParameterValue': args.key_name
            },
            {
                'ParameterKey': 'InstanceType',
                'ParameterValue': args.instance_type
            },
            {
                'ParameterKey': 'BitcoinRpcPassword',
                'ParameterValue': rpc_password
            },
            {
                'ParameterKey': 'Snapshot',
                'ParameterValue': args.snapshot_id
            },
            {
                'ParameterKey': 'Stage',
                'ParameterValue': args.stage
            },
            {
                'ParameterKey': 'Mode',
                'ParameterValue': args.mode
            },
            {
                'ParameterKey': 'HostNickName',
                'ParameterValue': host_nick_name
            },
        ],
        TimeoutInMinutes=timeout_in_minutes,
        Capabilities=[
            'CAPABILITY_IAM',
        ],
        OnFailure=args.on_failure
    )

if __name__ == '__main__':
    main()
