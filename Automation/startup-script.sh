#!/bin/sh

####################################
# Setting up environment variables #
####################################
# Variables used for Splunk connect for Kubernetes
export MONITORING_MACHINE='172.16.238.2'
export HEC_TOKEN='25577715-5282-4f8b-ab9c-c8aa95a75bea'
export HEC_PORT='30088'
export GLOBAL_HEC_INSECURE_SSL='true' 
export OBJECTS_INSECURE_SSL='true'
export METRICS_INSECURE_SSL='true' 
export JOURNALD_PATH='/run/log/journal' 
export KUBELET_PROTOCOL='https' 
export METRICS_INDEX='em_metrics'
export LOG_INDEX='main'
export META_INDEX='em_meta'
export CLUSTER_NAME='splunk-connector' 
export SCK_DOWNLOAD_ONLY='false' 
export HELM_RELEASE_NAME='helm'
export KUBERNETES_NAMESPACE='splunk-connector'
export CORE_OBJ='pods,nodes,component_statuses,config_maps,namespaces,persistent_volumes,persistent_volume_claims,resource_quotas,services,service_accounts,events' 
export APPS_OBJ='daemon_sets,deployments,replica_sets,stateful_sets' 

echo "==> Setting up Splunk connect for Kubernetes"
files="kubernetes_connect_template.yaml" "deploy_sck_k8s.sh" && for each in "${files[@]}"; do wget -O- --no-check-certificate http://splunk.traderyolo.com/en-US/static/app/splunk_app_infrastructure/kubernetes_connect/"$each" > $each; done && wget https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.3.0/splunk-connect-for-kubernetes-1.3.0.tgz -O splunk-connect-for-kubernetes.tgz && bash deploy_sck_k8s.sh
sleep 5 && echo " "

echo "==> Build Java app image and push it to docker registry"
docker compose -f ./Automation/java-app-docker-compose.yaml build
docker compose -f ./Automation/java-app-docker-compose.yaml push
sleep 10 && echo " "

echo "==> Deploying Java app in 'mem-leak-java' Namespace on Kubernetes env"
kubectl apply -f ./Automation/java-app-deployment.yaml

# moving to xMatter location
cd xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files
echo " " && echo "==> Build xMatters agent image and push it to docker registery"
docker compose -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/xmatter-docker-compose.yaml
docker compose -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/xmatter-docker-compose.yaml push
sleep 10 && echo " "

echo "==> Deploying roles, secret and xMatters agent in 'mem-leak-java' Namespace on Kubernetes env"
kubectl apply -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/xmatter-role.yaml
kubectl apply -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/kube/xagent-secrets.yaml
kubectl apply -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/kube/xagent-deploy.yaml