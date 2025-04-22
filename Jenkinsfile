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
        stage('Setup') {
            steps {
                script {
                    sh '''
                        if ! command -v docker-compose &> /dev/null; then
                            echo "Installing Docker Compose..."
                            curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                            chmod +x /usr/local/bin/docker-compose
                        fi
                    '''
                }
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
                echo 'Starting Docker services...'
                script {
                    if (isUnix()) {
                        sh 'docker-compose -p filecompressor up -d'  // Use filecompressor as project name
                    } else {
                        bat 'docker-compose -p filecompressor up -d'  // Use filecompressor as project name
                    }
                }
                echo 'Docker container started for filecompressor.'
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
            echo 'Cleaning up...'
            sh '''#!/bin/bash
                # Clean up any Docker resources
                docker-compose -p filecompressor down || true
            '''
        }
    }
}
