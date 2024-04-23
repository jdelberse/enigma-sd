#!/bin/bash

CPUS='1'
RAM='8G'
DISK='90G'

ROOT_DIR=/data/project/sleep_ENIGMA_deprivation/enigma-sd-glymphatic
LOGS_DIR=$ROOT_DIR/logs
WORK_DIR=/tmp

# print the .submit header
printf "# The environment
universe       = vanilla
getenv         = True
request_cpus   = ${CPUS}
request_memory = ${RAM}
request_disk   = ${DISK}

# Execution
executable     = $ROOT_DIR/code/move_data.sh\n
log       = ${LOGS_DIR}/\$(Cluster).\$(Process).${subid}.log.txt\n
output    = ${LOGS_DIR}/\$(Cluster).\$(Process).${subid}.out.txt\n
error     = ${LOGS_DIR}/\$(Cluster).\$(Process).${subid}.err.txt\n
Queue\n\n"