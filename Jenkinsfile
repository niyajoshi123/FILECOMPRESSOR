pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning GitHub repo...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build('filecompressor-app')
                }
            }
        }

        stage('Run Container') {
            steps {
                echo 'Running Docker container...'
                sh 'docker run -d -p 5000:5000 --name filecompressor filecompressor-app'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed.'
        }
        success {
            echo 'Pipeline succeeded.'
        }
    }
}
