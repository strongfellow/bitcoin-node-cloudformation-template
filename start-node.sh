#!/bin/bash

set -e
set -x

STACK_NAME="btc-2016-03-05-v-02"
VPC="vpc-599c723d"
SUBNET="subnet-09ee1e6d"
RPC_PASSWORD="ajfkldfdasf"
KEY_NAME="bitcoin-nodes"
INSTANCE_TYPE="c4.large"

TEMPLATE=node.json
# TEMPLATE=0mq-node.json

aws cloudformation create-stack \
  --stack-name ${STACK_NAME} \
  --template-body file://./${TEMPLATE} \
  --parameters ParameterKey=VPC,ParameterValue=${VPC} ParameterKey=Subnet,ParameterValue=${SUBNET} ParameterKey=BitcoinRpcPassword,ParameterValue=${RPC_PASSWORD} ParameterKey=KeyName,ParameterValue=${KEY_NAME} ParameterKey=InstanceType,ParameterValue=${INSTANCE_TYPE}

