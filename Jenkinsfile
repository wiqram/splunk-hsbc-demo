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
              }
          }
      }
      stage('Scan') {
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
                                ls
                              /home/jenkins/tools/io.snyk.jenkins.tools.SnykInstallation/snyk/snyk-linux auth "fb073e5e-9899-45d4-b3ba-78b203b493e9"
           /home/jenkins/tools/io.snyk.jenkins.tools.SnykInstallation/snyk/snyk-linux iac test compiled.yaml --severity-threshold=critical
           """,
              )
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