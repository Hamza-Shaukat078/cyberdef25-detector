pipeline {
    agent any

    triggers {
        // Auto-trigger when Git changes (polls every 5 minutes)
        pollSCM('H/5 * * * *')
    }

    environment {
        // Local image name
        IMAGE_NAME = "cyberdef25-detector"

        // Docker Hub repo (replace with your own username)
        DOCKERHUB_REPO = "hamzashaukat078/cyberdef25-detector:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building local Docker image...'
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Tag Image for Docker Hub') {
            steps {
                echo 'Tagging image for Docker Hub...'
                script {
                    sh 'docker tag $IMAGE_NAME $DOCKERHUB_REPO'
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo 'Logging in to Docker Hub...'
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_PASS'
                    )]) {
                        sh '''
                          echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        '''
                    }
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    sh 'docker push $DOCKERHUB_REPO'
                }
            }
        }

        stage('Run with Docker Compose') {
            steps {
                echo 'Running malware detection with Docker Compose...'
                script {
                    sh 'docker-compose down || true'
                    // Optional: ensure latest image is pulled
                    sh 'docker-compose pull || true'
                    sh 'docker-compose up -d --build'
                    sh 'sleep 10'
                    sh 'docker-compose ps'
                    sh 'cat output/alerts.csv || echo "Processing..."'
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            script {
                sh 'docker-compose down || true'
                sh 'docker system prune -af --volumes || true'
            }
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}

