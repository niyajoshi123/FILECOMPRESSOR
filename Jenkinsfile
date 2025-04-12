pipeline {
    agent any

    environment {
        // Set up any environment variables you might need
        PROJECT_REPO = 'https://github.com/niyajoshi123/FILECOMPRESSOR.git'
        BRANCH = 'main' // Change if you're using another branch
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: "${BRANCH}", url: "${PROJECT_REPO}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt || echo "No requirements.txt found"
                '''
            }
        }

        stage('Build/Run Project') {
            steps {
                sh '''
                    source venv/bin/activate
                    python app.py || python3 app.py
                '''
            }
        }
    }
}

