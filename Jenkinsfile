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
                    which python3
                    python3 --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                    # Attempt to install python3-venv (for Ubuntu/Debian)
                    if command -v apt-get &> /dev/null; then
                        echo "Using apt-get to install python3-venv"
                        sudo apt-get update
                        sudo apt-get install -y python3-venv
                    # For systems using yum (CentOS/RHEL)
                    elif command -v yum &> /dev/null; then
                        echo "Using yum to install python3-venv"
                        sudo yum install -y python3-venv
                    else
                        echo "Could not determine package manager"
                    fi
                '''
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''#!/bin/bash
                    # Remove existing venv if any
                    if [ -d "venv" ]; then
                        rm -rf venv
                    fi
                    
                    # Create virtual environment
                    echo "Creating virtual environment with python3 -m venv venv"
                    python3 -m venv venv
                    
                    # Check if venv was created
                    if [ -f "venv/bin/activate" ]; then
                        echo "Virtual environment created successfully"
                        . venv/bin/activate
                        python --version
                        
                        # Check if requirements.txt exists
                        if [ -f "requirements.txt" ]; then
                            echo "Installing requirements from requirements.txt"
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        else
                            echo "WARNING: requirements.txt not found"
                            # Install basic Flask requirements
                            pip install flask
                        fi
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
                        # Check if app.py exists
                        if [ -f "app.py" ]; then
                            echo "Starting Flask app with app.py"
                            FLASK_APP=app.py nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                        else
                            echo "Looking for other Flask entry points..."
                            # Find possible Flask app entry points
                            for file in $(find . -maxdepth 1 -name "*.py"); do
                                echo "Found Python file: $file"
                                if grep -q "app = Flask" "$file"; then
                                    echo "Starting Flask app with $file"
                                    FLASK_APP=$file nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                                    break
                                fi
                            done
                        fi
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
                    # Check if app is running
                    if curl --fail http://localhost:5000; then
                        echo "App is reachable"
                    else
                        echo "App not reachable"
                        exit 1
                    fi
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