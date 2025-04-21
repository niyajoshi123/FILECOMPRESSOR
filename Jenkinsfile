pipeline {
    agent any
    
    stages {
        stage('Clone & Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'filecompressor',
                    url: 'https://github.com/niyajoshi123/FILECOMPRESSOR.git'
                echo 'Repository cloned successfully'
            }
        }
        
        stage('Build') {
            steps {
                sh '''#!/bin/bash
                    # Install dependencies
                    python3 -m pip install --user flask
                    if [ -f "requirements.txt" ]; then
                        python3 -m pip install --user -r requirements.txt
                    fi
                    echo 'Build completed successfully'
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''#!/bin/bash
                    # Run simple tests to verify the app
                    python3 -c "import flask; print('Flask imported successfully')"
                    # Add more tests as needed
                    echo 'Tests passed successfully'
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''#!/bin/bash
                    # Kill any existing Flask processes
                    pkill -f "python3 -m flask run" || true
                    
                    # Find the Flask app file
                    if [ -f "app.py" ]; then
                        export FLASK_APP=app.py
                    else
                        export FLASK_APP=$(find . -name "*.py" -type f -exec grep -l "Flask" {} \\; | head -1)
                    fi
                    
                    # Run Flask app in background
                    nohup python3 -m flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &
                    echo $! > flask.pid
                    echo 'Application deployed successfully'
                '''
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline succeeded! Application deployed successfully.'
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