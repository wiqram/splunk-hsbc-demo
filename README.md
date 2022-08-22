# splunk-hsbc-demo
This demo has the below steps - 
1) Setting up Splunk
2) Configuring Splunk Alerts and Apps
3) Step 1 and 2 are done via Jenkinsfile, additionally the configurations are saved across restarts through persistent volume
4) Configure splunk-infrastructure by running the below command within the Automation/splunk-monitor folder
   
export MONITORING_MACHINE='splunk.splunk.svc.cluster.local' && export HEC_TOKEN='25577715-5282-4f8b-ab9c-c8aa95a75bea' && export HEC_PORT='8088' && export GLOBAL_HEC_INSECURE_SSL='true' && export OBJECTS_INSECURE_SSL='true' && export METRICS_INSECURE_SSL='true' && export JOURNALD_PATH='/run/log/journal' && export KUBELET_PROTOCOL='http' && export METRICS_INDEX='em_metrics' && export LOG_INDEX='main' && export META_INDEX='em_meta' && export CLUSTER_NAME='minikube' && export SCK_DOWNLOAD_ONLY='false' && export HELM_RELEASE_NAME='helm' && export KUBERNETES_NAMESPACE='splunk-connect' && export CORE_OBJ='pods,nodes,component_statuses,config_maps,namespaces,persistent_volumes,persistent_volume_claims,resource_quotas,services,service_accounts,events' && export APPS_OBJ='daemon_sets,deployments,replica_sets,stateful_sets' && files=("kubernetes_connect_template.yaml" "deploy_sck_k8s.sh") && for each in "${files[@]}"; do wget -O- --no-check-certificate https://splunk.traderyolo.com:/en-US/static/app/splunk_app_infrastructure/kubernetes_connect/"$each" > $each; done && wget https://github.com/splunk/splunk-connect-for-kubernetes/releases/download/1.3.0/splunk-connect-for-kubernetes-1.3.0.tgz -O splunk-connect-for-kubernetes.tgz && bash deploy_sck_k8s.sh

5) also via jenkinsfile, deploy xmatter agent into the same namespace as the mem leak java code
