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

        stage('Install Dependencies') {
            steps {
                sh '''#!/bin/bash
                    python3 -m pip install --user flask
                    if [ -f "requirements.txt" ]; then
                        python3 -m pip install --user -r requirements.txt
                    fi
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''#!/bin/bash
                    # Kill any existing Flask processes
                    pkill -f "python3 -m flask run" || true
                    
                    # Find Flask app file
                    if [ -f "app.py" ]; then
                        export FLASK_APP=app.py
                    else
                        # Use the first Python file with Flask import
                        export FLASK_APP=$(grep -l "from flask import" *.py | head -1)
                    fi
                    
                    # Run Flask app in background
                    nohup python3 -m flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                    echo $! > flask.pid
                    sleep 3
                    cat flask.log
                '''
                echo 'Flask app started'
            }
        }

        stage('Verify App') {
            steps {
                sh '''#!/bin/bash
                    curl -s http://localhost:5000
                '''
            }
        }
    }

    post {
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