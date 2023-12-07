pipeline {
  /* agent //any
   {
    kubernetes {
        cloud 'kubernetes'
        label 'kubeagent'
        defaultContainer 'jnlp'
      }
    } */
    agent none
  stages {
      /* stage('Shutdown Splunk') {
       agent {
              kubernetes {
                  cloud 'kubernetes'
                  label 'kubeagent'
                  defaultContainer 'jnlp'
                }
             }
          steps {
              script {
                  //kubernetesDeploy(configs: "compiled.yaml", kubeconfigId: "jenkins-kubeconfig-file", deleteResource: true)
                  sh 'kubectl delete --ignore-not-found=true -f compiled.yaml'
                  sleep(time:30,unit:"SECONDS")
              }
          }
      } */
     /* stage("install helm"){
        steps{
             sh 'find -type f -name "helm-v3.6.1-linux-amd64*" -delete'
             sh 'wget https://get.helm.sh/helm-v3.6.1-linux-amd64.tar.gz'
             sh 'ls -a'
             sh 'tar -xvzf helm-v3.6.1-linux-amd64.tar.gz'
             sh './linux-amd64/helm version'
              *//*
             sh 'sudo cp linux-amd64/helm /usr/bin'
             sh 'curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3'
             sh 'chmod 700 get_helm.sh'
             sh './get_helm.sh'
             sh 'helm version' *//*
        }
    } */
      /* stage('Vulnerability Scan') {
       agent {
              kubernetes {
                  cloud 'kubernetes'
                  label 'kubeagent'
                  defaultContainer 'jnlp'
                }
             }
       steps {
            echo 'Testing...'
             snykSecurity(
                snykInstallation: 'snyk',
                //organisation: 'jeveenjacob',
                snykTokenId: 'snyk',
                failOnError: false,
                failOnIssues: false,
                targetFile: 'package.json'
                // place other parameters here
            )
            echo "Security check initiated"
            sh(
              script:
                      """\
                      /home/jenkins/tools/io.snyk.jenkins.tools.SnykInstallation/snyk/snyk-linux auth "fb073e5e-9899-45d4-b3ba-78b203b493e9"
                       /home/jenkins/tools/io.snyk.jenkins.tools.SnykInstallation/snyk/snyk-linux iac test compiled.yaml --severity-threshold=critical
                       """,
              )
            echo "Security check done"
        }
        } */
    /* stage('Deploy Splunk Configs') {
     agent {
            kubernetes {
                cloud 'kubernetes'
                label 'kubeagent'
                defaultContainer 'jnlp'
              }
           }
      steps {
               script {
                     //kubernetesDeploy(configs: "splunk-namespace.yaml", kubeconfigId: "jenkins-kubeconfig-file")
                     //kubernetesDeploy(configs: "publisher-deleter-cronjob.yaml", kubeconfigId: "jenkins-kubeconfig-file")
                     //kubernetesDeploy(configs: "compiled.yaml", kubeconfigId: "jenkins-kubeconfig-file")
                     sh 'kubectl apply -f splunk-namespace.yaml'
                     sh 'kubectl apply -f compiled.yaml'
                     sleep(time:30,unit:"SECONDS")
               }
            }
        } */
       /*
       JEVEEN TO WORK ON THIS DOCKER COMPOSE STEP OF PIPELINE
       stage('Build and Push Docker Images') {
             agent {
                    kubernetes {
                        cloud 'kubernetes'
                        label 'kubeagent'
                        defaultContainer 'jnlp'
                      }
                   }
              steps {
                       //docker compose build -d file
                       //docker compose push -f file
                    }
                } */
    stage('Automation infra deployment') {
     agent {
            kubernetes {
                cloud 'kubernetes'
                label 'kubeagent'
                defaultContainer 'jnlp'
              }
           }
      steps {
               echo "Automation script execution started"
               sh(
                  script:
                         """\
                        kubectl apply -f ./Automation/namespace-mem-leak.yaml
                        kubectl apply -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/xmatter-role.yaml
                        kubectl apply -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/kube/xagent-secrets.yaml
                        kubectl apply -f ./Automation/xMatters_k8_stuff/xm-labs-xagent-on-kubernetes-master/files/kube/xagent-deploy.yaml
                        kubectl apply -f ./Automation/java-app-deployment.yaml
                         """,
                      )
                echo "Automation script execution done"      
            }
        }
    }
}
