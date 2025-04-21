pipeline {
    agent any

    environment {
        // Add your environment variables here if needed
        FLASK_APP = "app.py"
        FLASK_ENV = "development"
    }

    stage('Clone Repository') {
    steps {
        git credentialsId: 'filecompressor', url: 'https://github.com/niyajoshi123/FILECOMPRESSOR.git'
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
                echo 'Make sure your database (PostgreSQL/MySQL) is running and configured.'
                // Optional: You can add db init scripts here
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    source venv/bin/activate
                    nohup flask run --host=0.0.0.0 --port=5000 &
                '''
                echo 'Flask server is running in the background.'
            }
        }

        stage('Post-deployment verification') {
            steps {
                sh '''
                    curl --fail http://localhost:5000 || echo "App is not reachable!"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ File Compression App deployed successfully!'
        }
        failure {
            echo '❌ Deployment failed. Please check logs.'
        }
    }
}
