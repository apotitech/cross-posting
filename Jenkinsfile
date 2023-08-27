pipeline {
    agent any
    environment {
        DOCKER_HUB_USERNAME = 'apotieri'
        DOCKER_IMAGE_NAME = 'trivy_scanned_image'
        TRIVY_TEMPLATE_PATH = "/home/jenkins/trivy_template.tpl"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME .'
                }
            }
        }

        stage('Trivy Scan Local Image') {
            steps {
                script {
                    def trivyExitCode = sh(script: "trivy image --format template --template \"@${env.TRIVY_TEMPLATE_PATH}\" --output trivy_local_report.html ${env.DOCKER_HUB_USERNAME}/${env.DOCKER_IMAGE_NAME}", returnStatus: true)
                    if (trivyExitCode != 0) {
                        error("Trivy detected vulnerabilities in the image!")
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy_local_report.html', allowEmptyArchive: true
                }
            }
        }

        stage('Trivy Scan DockerHub Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerID', passwordVariable: 'DOCKER_PWD', usernameVariable: 'DOCKER_USER')]) {
                    script {
                        sh 'docker login -u $DOCKER_USER -p $DOCKER_PWD'
                        def trivyExitCode = sh(script: "trivy image --format template --template \"@${env.TRIVY_TEMPLATE_PATH}\" --output trivy_dockerhub_report.html ${env.DOCKER_HUB_USERNAME}/${env.DOCKER_IMAGE_NAME}", returnStatus: true)
                        sh 'docker logout'
                        if (trivyExitCode != 0) {
                            error("Trivy detected vulnerabilities in the image!")
                        }
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy_dockerhub_report.html', allowEmptyArchive: true
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: "trivy_dockerhub_report.html", fingerprint: true
            publishHTML (target: [
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'trivy_dockerhub_report.html',
                reportName: 'Trivy Scan',
            ])
        }
    }
}
