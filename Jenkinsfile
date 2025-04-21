pipeline {
    agent any


    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository'
                // git 'https://github.com/Sanamniyas/sample.git'  // Modify with your repo URL
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project'
               // sh './gradlew build'  // Modify with your build tool/command (e.g., Maven, Gradle, npm)
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests'
              //  sh './gradlew test'  // Modify with your test command
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying to server'
               // sh "scp -r ${BUILD_DIR}/* ${DEPLOY_SERVER}:/path/to/deploy/directory"  // Modify for your deployment command
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}