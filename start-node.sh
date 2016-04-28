#!/bin/bash

set -e
set -x

NODE_TYPE="baked-node"

TIMESTAMP=`date +%s`
DATE=`date +%Y-%m-%d`
STACK_NAME=btc-${NODE_TYPE}-${DATE}-${TIMESTAMP}
echo ${STACK_NAME}
TEMPLATE=${NODE_TYPE}.json
echo ${TEMPLATE}

VPC="vpc-599c723d"
SUBNET="subnet-09ee1e6d"
RPC_PASSWORD="ajfkldfdasf"
KEY_NAME="thinkpad"
INSTANCE_TYPE="m3.medium"
SNAPSHOT="snap-c2367687"

# DO_NOTHING | ROLLBACK | DELETE
ON_FAILURE=DO_NOTHING

aws cloudformation create-stack \
  --capabilities CAPABILITY_IAM \
  --stack-name ${STACK_NAME} \
  --template-body file://./${TEMPLATE} \
  --on-failure ${ON_FAILURE} \
  --parameters ParameterKey=VPC,ParameterValue=${VPC} \
               ParameterKey=Subnet,ParameterValue=${SUBNET} \
               ParameterKey=KeyName,ParameterValue=${KEY_NAME} \
               ParameterKey=InstanceType,ParameterValue=${INSTANCE_TYPE} \
               ParameterKey=BitcoinRpcPassword,ParameterValue=${RPC_PASSWORD} \
              ParameterKey=Snapshot,ParameterValue=${SNAPSHOT}
