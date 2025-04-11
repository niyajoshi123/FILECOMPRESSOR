pipeline {
    agent any

    environment {
        // Set virtual environment path (optional)
        VENV = 'venv'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning GitHub repo...'
                checkout scm
            }
        }

        stage('Install Requirements') {
            steps {
                echo 'Installing dependencies...'
                sh 'python -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Testing basic Flask server run...'
                sh './venv/bin/python -m flask --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t filecompressor-app .'
            }
        }

        stage('Deploy (Run Container)') {
            steps {
                echo 'Running Docker container...'
                sh 'docker run -d -p 5000:5000 --name filecompressor filecompressor-app'
            }
        }
    }

    post {
        success {
            echo 'Pipeline ran successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
