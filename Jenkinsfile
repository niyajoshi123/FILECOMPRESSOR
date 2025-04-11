pipeline {
    agent {
        docker {
            image 'docker:24.0.5-dind' // or another version you prefer
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

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
                sh 'docker build -t file-compressor .'
            }
        }

        stage('Run Container') {
            steps {
                echo 'Running Docker container...'
                sh 'docker run -d -p 5000:5000 file-compressor'
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
