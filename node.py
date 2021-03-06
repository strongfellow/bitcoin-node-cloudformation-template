
import argparse
import sys
import uuid

import boto3

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--network', default='main', choices=['main', 'testnet3', 'segnet'])
    parser.add_argument('--region', default='us-west-2')
    parser.add_argument('--volume-size', help='the size in GB of the data volume', type=int)
    parser.add_argument('--az', default='us-west-2a')
    parser.add_argument('--nickname', required=True)
    parser.add_argument('--mode',
                        required=True,
                        choices=['AWSListener', 'EdgeNode', 'Webapp', 'Explorer', 'WhiteLabel' ])
    parser.add_argument('--stage',
                        required=True,
                        choices=['dev', 'test', 'staging', 'prod'])

    parser.add_argument('--instance-type', required=True)
    parser.add_argument('--bitcoin-version',
                        default='v0dot12dot1',
                        choices=['v0dot12dot1'])

    parser.add_argument('--on-failure',
                        default='DO_NOTHING',
                        choices=['DO_NOTHING', 'ROLLBACK', 'DELETE'])
    parser.add_argument('--vpc',
                        default='vpc-599c723d')
    parser.add_argument('--subnet',
                        default='subnet-09ee1e6d')
    parser.add_argument('--snapshot-id', required=True)
    parser.add_argument('--key-name',
                        default='thinkpad')
    args = parser.parse_args(args)

    volume_size = args.volume_size
    if volume_size is None:
        volume_size = 120 if args.network == 'main' else 40

    stack_name = '{nickname}-{mode}'.format(
        nickname=args.nickname,
        mode=args.mode)
    host_nick_name = stack_name
    timeout_in_minutes = 15

    rpc_password = str(uuid.uuid4())

    body = open('baked-node.json').read()

    client = boto3.client('cloudformation', region_name=args.region)
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
                'ParameterKey': 'AZ',
                'ParameterValue': args.az
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
                'ParameterKey': 'BitcoinVersion',
                'ParameterValue': args.bitcoin_version
            },
            {
                'ParameterKey': 'Snapshot',
                'ParameterValue': args.snapshot_id if args.snapshot_id.startswith('s-') else 'NO_SNAPSHOT_ID'
            },
            {
                'ParameterKey': 'VolumeSize',
                'ParameterValue': str(volume_size)
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
            {
                'ParameterKey': 'BitcoinNetwork',
                'ParameterValue': args.network
            },
            {
                'ParameterKey': 'BitcoinPort',
                'ParameterValue': '18333' if args.network == 'testnet3' else '8333'
            },
            {
                'ParameterKey': 'BitcoinRpcPort',
                'ParameterValue': '18332' if args.network == 'testnet3' else '8332'
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
