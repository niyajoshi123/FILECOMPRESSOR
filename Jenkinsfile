pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/niyajoshi123/FILECOMPRESSOR.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Your build steps go here...'
            }
        }
    }
}
