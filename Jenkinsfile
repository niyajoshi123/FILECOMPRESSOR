pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning GitHub repo...'
                checkout scm
            }
        }

        stage('Install System Dependencies') {
            steps {
                echo 'Installing system dependencies...'
                sh '''
                    apt-get update
                    apt-get install -y python3-venv python3-dev default-libmysqlclient-dev build-essential pkg-config
                '''
            }
        }

        stage('Install Requirements') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t filecompressor:latest .'
            }
        }

        stage('Deploy (Run Container)') {
            steps {
                echo 'Running Docker container...'
                sh 'docker run -d -p 5000:5000 filecompressor:latest'
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed.'
        }
    }
}
