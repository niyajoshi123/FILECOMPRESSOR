pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', // Change 'master' to 'main' here
                    credentialsId: 'filecompressor',
                    url: 'https://github.com/niyajoshi123/FILECOMPRESSOR.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Database Setup') {
            steps {
                echo 'Make sure your PostgreSQL/MySQL is configured'
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    source venv/bin/activate
                    nohup flask run --host=0.0.0.0 --port=5000 &
                '''
                echo 'Flask app started'
            }
        }

        stage('Post-deployment Verification') {
            steps {
                sh '''
                    curl --fail http://localhost:5000 || echo "App not reachable"
                '''
            }
        }
    }

      post {
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
