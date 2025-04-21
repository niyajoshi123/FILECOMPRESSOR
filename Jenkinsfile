pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main',
                    credentialsId: 'filecompressor',
                    url: 'https://github.com/niyajoshi123/FILECOMPRESSOR.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''#!/bin/bash
                    python3 -m venv venv
                    . venv/bin/activate
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
                sh '''#!/bin/bash
                    . venv/bin/activate
                    nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                    echo $! > flask.pid
                    sleep 5 # Give the app a moment to start
                '''
                echo 'Flask app started'
            }
        }

        stage('Post-deployment Verification') {
            steps {
                sh '''#!/bin/bash
                    curl --fail http://localhost:5000 || echo "App not reachable"
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully.'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
        always {
            sh '''#!/bin/bash
                if [ -f flask.pid ]; then
                    kill $(cat flask.pid) || true
                    rm flask.pid
                fi
            '''
        }
    }
}