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
      stage('Delete App') {
          steps {
              script {
                  kubernetesDeploy(configs: "compiled.yaml", kubeconfigId: "jenkins-kubeconfig-file", deleteResource: true)
                  sleep(time:30,unit:"SECONDS")
                  //kubernetesDeploy(configs: "yolo-namespace.yaml", kubeconfigId: "jenkins-kubeconfig-file", deleteResource: true)
                  //sleep(time:3,unit:"SECONDS")
              }
          }
      }
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
      /*stage('Security Check') {
          steps {
              echo "Security check initiated"
              sh(
                      script:
                              """\
           
           """,
              )
              sleep(time: 5, unit: "SECONDS")
              echo "Security check done"
          }
      }*/
    stage('Scan') {
               steps {
                    echo 'Testing...'
                     snykSecurity(
                        snykInstallation: 'snyk',
                        organisation: 'jeveenjacob', 
                        snykTokenId: '34e37d85-0cd6-4aa6-a9c6-a14aa9f7c99b',
                        failOnError: false, 
                        failOnIssues: false,
                        targetFile: 'compiled.yaml'
                        // place other parameters here
                    )
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