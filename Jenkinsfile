pipeline {
    agent any

    triggers {
        // Poll SCM every 5 minutes; if changes, pipeline runs
        pollSCM('H/5 * * * *')
    }

    environment {
        IMAGE_NAME = "cyberdef25-detector"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Run with Docker Compose') {
            steps {
                echo 'Running malware detection with Docker Compose...'
                script {
                    sh 'docker-compose down || true'
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
            sh 'docker-compose down || true'
            sh 'docker system prune -af --volumes || true'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
