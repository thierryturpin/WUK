#!/bin/bash
sudo yum -y update
sudo yum install -y ruby
sudo yum install -y aws-cli

echo 'Yum install of ruby and aws-cli done'

cd ~
aws s3 cp s3://aws-codedeploy-us-east-2/latest/install . --region us-east-2
chmod +x ./install

echo 'Starting install of codedeploy'

sudo ./install auto

echo 'Install of codedeploy done'


# check for master node
IS_MASTER=true
if [ -f /mnt/var/lib/info/instance.json ]
then
	IS_MASTER=`cat /mnt/var/lib/info/instance.json | jq -c '.isMaster'`
fi

# only run if master node
if [ "$IS_MASTER" = true ]; then
    echo 'Running on master node'

fi
