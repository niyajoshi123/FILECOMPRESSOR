pipeline {
    agent any
    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/niyajoshi123/FILECOMPRESSOR.git', branch: 'main'
            }
        }
        stage('Run Project') {
            steps {
                sh 'ls -la' // or whatever build command
            }
        }
    }
}
