#!/bin/bash

set -e
set -x

NODE_TYPE="bitcoin-install"

TIMESTAMP=`date +%s`
DATE=`date +%Y-%m-%d`
STACK_NAME=btc-${NODE_TYPE}-${DATE}-${TIMESTAMP}
TEMPLATE=${NODE_TYPE}.json

VPC="vpc-599c723d"
SUBNET="subnet-09ee1e6d"
KEY_NAME="thinkpad"
INSTANCE_TYPE="c4.2xlarge"

# DO_NOTHING | ROLLBACK | DELETE
ON_FAILURE=DO_NOTHING

aws cloudformation create-stack \
  --stack-name ${STACK_NAME} \
  --template-body file://./${TEMPLATE} \
  --on-failure ${ON_FAILURE} \
  --parameters ParameterKey=VPC,ParameterValue=${VPC} \
               ParameterKey=Subnet,ParameterValue=${SUBNET} \
               ParameterKey=KeyName,ParameterValue=${KEY_NAME} \
               ParameterKey=InstanceType,ParameterValue=${INSTANCE_TYPE}
