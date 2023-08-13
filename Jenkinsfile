pipeline {
    agent any
    }

    stages {
        stage('Deploy on Kubernetes') {
            steps {
                script {
                    sh """
                        kubectl get nodes
                    """
                }
            }
        }
    }
