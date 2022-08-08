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
                  sleep(time:5,unit:"SECONDS")
                  //kubernetesDeploy(configs: "yolo-namespace.yaml", kubeconfigId: "jenkins-kubeconfig-file", deleteResource: true)
                  //sleep(time:3,unit:"SECONDS")
              }
          }
      }
      stage('Copy App') {
          echo "copying folder started"
          sh (
           script:
           """\
           cp mnt/jenkins/workspace/splunkdemo mnt/splunk-hsbc\
           """,
           )
          sleep(time:5,unit:"SECONDS")
           echo "copying folder done"
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