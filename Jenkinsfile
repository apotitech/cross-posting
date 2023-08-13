pipeline {
    agent any

    environment {
        DOCKER_HUB_USERNAME = 'apotieri'
        DOCKER_IMAGE_NAME = 'CompleteCICD'
        KOPS_CLUSTER_NAME = 'apotiankops7.k8s.local'
        KOPS_STATE_STORE = 's3://apotiankops7.k8s.local'
        DEPLOYMENT_FILE_PATH = 'deployment.yaml' // path to your deployment file in the repo
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:latest .'
                }
            }
        }

        stage('DOCKER PUSH') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'pwd', usernameVariable: 'user')]) {
                   sh "docker login -u ${user} -p ${pwd}"
                   sh "docker push apotieri/app_maven_001"
                    }                    
            }
        }

        stage('Create Kops Cluster') {
            steps {
                script {
                    sh """
                        kops create cluster --zones us-east-1a --master-size t2.medium --master-count 1 --node-size t2.medium --node-count=2 --name=$KOPS_CLUSTER_NAME --state=$KOPS_STATE_STORE --yes
                        kops update cluster --name=$KOPS_CLUSTER_NAME --state=$KOPS_STATE_STORE --yes
                        kops validate cluster --wait 10m
                    """
                }
            }
        }

        stage('Deploy on Kubernetes') {
            steps {
                script {
                    sh """
                        kubectl apply -f $DEPLOYMENT_FILE_PATH
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker rmi $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:latest'
            sh 'kubectl get all'
            // Optionally, you can delete the cluster after deployment
            sh "kops delete cluster --name=$KOPS_CLUSTER_NAME --state=$KOPS_STATE_STORE --yes"
        }
    }
}
