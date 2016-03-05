#!/bin/bash

set -e
set -x

STACK_NAME="btc-2016-03-04-v-02"
VPC="vpc-599c723d"
SUBNET="subnet-09ee1e6d"
RPC_PASSWORD="ajfkldfdasf"
KEY_NAME="bitcoin-nodes"
INSTANCE_TYPE="c4.large"

aws cloudformation create-stack \
  --stack-name ${STACK_NAME} \
  --template-body file://./0mq-node.json \
  --parameters ParameterKey=VPC,ParameterValue=${VPC} ParameterKey=Subnet,ParameterValue=${SUBNET} ParameterKey=BitcoinRpcPassword,ParameterValue=${RPC_PASSWORD} ParameterKey=KeyName,ParameterValue=${KEY_NAME} ParameterKey=InstanceType,ParameterValue=${INSTANCE_TYPE}

