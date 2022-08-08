pipeline {
  agent //any
   {
    kubernetes {
        cloud 'kubernetes'
        label 'kubeagent'
        defaultContainer 'jnlp'
      }
    }
  stages {
      /*stage('Delete App') {
          steps {
              script {
                  kubernetesDeploy(configs: "compiled.yaml", kubeconfigId: "jenkins-kubeconfig-file", deleteResource: true)
                  sleep(time:5,unit:"SECONDS")
                  //kubernetesDeploy(configs: "yolo-namespace.yaml", kubeconfigId: "jenkins-kubeconfig-file", deleteResource: true)
                  //sleep(time:3,unit:"SECONDS")
              }
          }
      }*/
      /*stage('Copy App') {
          steps {
              echo "copying folder started"
              sh(
                      script:
                              """\
           cp -r mnt/jenkins/workspace/splunkdemo mnt/splunk-hsbc\
           """,
              )
              sleep(time: 5, unit: "SECONDS")
              echo "copying folder done"
          }
      }*/
      stage('Security Check') {
          steps {
              echo "Security check initiated"
              sh(
                      script:
                              """\
           sudo apt install curl -y
           curl https://static.snyk.io/cli/latest/snyk-linux -o snyk
           chmod +x ./snyk
           ./snyk auth "b7503882-a832-4284-9b0b-17a4f20f2bb1"
           ./snyk iac test compiled.yaml --severity-threshold=critical
           """,
              )
              sleep(time: 5, unit: "SECONDS")
              echo "Security check done"
          }
      }

    stage('Deploy App') {
      steps {
               script {
                     kubernetesDeploy(configs: "splunk-namespace.yaml", kubeconfigId: "jenkins-kubeconfig-file")
                     //kubernetesDeploy(configs: "publisher-deleter-cronjob.yaml", kubeconfigId: "jenkins-kubeconfig-file")
                     kubernetesDeploy(configs: "compiled.yaml", kubeconfigId: "jenkins-kubeconfig-file")
               }
            }
        }
    }
}