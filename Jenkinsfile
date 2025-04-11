pipeline {
    agent any

    environment {
        APP_NAME = "filecompressor"
        IMAGE_NAME = "filecompressor-image"
        CONTAINER_NAME = "filecompressor-container"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Cloning GitHub repo..."
                checkout scm
            }
        }

        stage('Install Requirements') {
            steps {
                echo "Installing dependencies..."
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh '''
                    docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Deploy (Run Container)') {
            steps {
                echo "Running Docker container..."
                sh '''
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME
                '''
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed."
        }
        success {
            echo "Pipeline executed successfully."
        }
    }
}
