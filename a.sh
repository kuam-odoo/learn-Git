#!/bin/bash

# Description: This script runs a specified command

# The command to run
command_to_run="cd "
cmnd1="cd odoo/community"
cmnd2="git fetch --all"
cmnd3="git pull"
# Execute the command
# Check if the command was successful
CURRENT_DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Echo the date
echo "The last fetch pull was on date and time is: $CURRENT_DATE" >> ./a.txt

echo "Running command: fetch and pull in community and enterprise both"
$command_to_run
$cmnd1
pwd
$cmnd2
$cmnd3
cd ..
cd enterprise
pwd
$cmnd2
$cmnd3

if [ $? -eq 0 ]; then
  echo "Command executed successfully."
else
  echo "Command failed with exit code $?."
fi
