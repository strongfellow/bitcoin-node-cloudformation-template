#!/bin/bash

set -e
set -x

#NODE_TYPE="0mq-"
#NODE_TYPE=""
#NODE_TYPE="baked-"
NODE_TYPE=""

TIMESTAMP=`date +%s`
DATE=`date +%Y-%m-%d`
STACK_NAME=btc-${NODE_TYPE}${DATE}-${TIMESTAMP}
echo ${STACK_NAME}
TEMPLATE=${NODE_TYPE}node.json
echo ${TEMPLATE}

VPC="vpc-599c723d"
SUBNET="subnet-09ee1e6d"
RPC_PASSWORD="ajfkldfdasf"
KEY_NAME="bitcoin-nodes"
#INSTANCE_TYPE="c4.2xlarge"
INSTANCE_TYPE="m3.medium"
SNAPSHOT="snap-73cde52f"

# DO_NOTHING | ROLLBACK | DELETE
ON_FAILURE=DO_NOTHING

aws cloudformation create-stack \
  --capabilities CAPABILITY_IAM \
  --stack-name ${STACK_NAME} \
  --template-body file://./${TEMPLATE} \
  --on-failure ${ON_FAILURE} \
  --parameters ParameterKey=VPC,ParameterValue=${VPC} \
               ParameterKey=Subnet,ParameterValue=${SUBNET} \
               ParameterKey=BitcoinRpcPassword,ParameterValue=${RPC_PASSWORD} \
               ParameterKey=KeyName,ParameterValue=${KEY_NAME} \
               ParameterKey=InstanceType,ParameterValue=${INSTANCE_TYPE} \
               ParameterKey=Snapshot,ParameterValue=${SNAPSHOT}
