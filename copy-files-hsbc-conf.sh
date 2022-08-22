#!/bin/sh

while inotifywait -r /home/cloud/Ideaprojects/minikube-mnt/jenkins/workspace/splunkdemo/hsbc_wpb_acs/local/*; do
#rsync -avu --delete    
#echo "password" | sudo rsync -avz --delete /home/cloud/Ideaprojects/minikube-mnt/jenkins/workspace/splunkdemo/hsbc_wpb_acs/local /home/cloud/Ideaprojects/minikube-mnt/splunk-hsbc/hsbc_wpb_acs
echo "3142" | sudo -S cp /home/cloud/Ideaprojects/minikube-mnt/jenkins/workspace/splunkdemo/hsbc_wpb_acs/local/savedsearches.conf /home/cloud/Ideaprojects/minikube-mnt/splunk-hsbc/hsbc_wpb_acs/local/
done
