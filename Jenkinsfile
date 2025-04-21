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

        stage('Check Python Installation') {
            steps {
                sh '''#!/bin/bash
                    which python3 || echo "Python3 not found"
                    python3 --version || echo "Could not get Python version"
                '''
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''#!/bin/bash
                    # Check if venv directory exists and remove it if it does
                    if [ -d "venv" ]; then
                        rm -rf venv
                    fi
                    
                    # Create virtual environment
                    python3 -m venv venv || echo "Failed to create virtual environment"
                    
                    # Check if virtual environment was created
                    if [ -f "venv/bin/activate" ]; then
                        echo "Virtual environment created successfully"
                        . venv/bin/activate
                        python --version
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    else
                        echo "Virtual environment creation failed"
                        exit 1
                    fi
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
                    if [ -f "venv/bin/activate" ]; then
                        . venv/bin/activate
                        nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                        echo $! > flask.pid
                        sleep 5 # Give the app a moment to start
                    else
                        echo "Virtual environment not found"
                        exit 1
                    fi
                '''
                echo 'Flask app started'
            }
        }

        stage('Post-deployment Verification') {
            steps {
                sh '''#!/bin/bash
                    curl --fail http://localhost:5000 || (echo "App not reachable" && exit 1)
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