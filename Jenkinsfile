pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository'
                git 'https://github.com/niyajoshi123/FILECOMPRESSOR.git'  // Replace with your repo URL
            }
        }

        stage('Build') {
            steps {
                echo 'Installing dependencies and building the project'
                sh 'npm install'  // Install dependencies for the Node.js project
                sh 'npm run build'  // Run build command (if defined in package.json)
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests'
                sh 'npm test'  // Run tests using npm (ensure you have a test script in package.json)
            }
        }

        stage('Deploy') {
            steps {
                echo 'Building Docker image and deploying to server'

                // Build Docker image
                sh 'docker build -t filecompressor-app .'  // Build the Docker image

                // Push the Docker image (Optional: if you're pushing to a registry)
                // sh 'docker push filecompressor-app'  // Uncomment if pushing to Docker Hub or another registry

                // Deploy the Docker container
                sh 'docker run -d -p 80:80 filecompressor-app'  // Run the container on port 80 (adjust ports as needed)

                // Optional: If deploying to a remote server via Docker, use SCP to copy Docker image or files (if necessary)
                // sh "scp filecompressor-app.tar your-server-ip-or-url:/path/to/deploy/directory"  // Uncomment and adjust if needed
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
