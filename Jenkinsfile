pipeline {
  agent any

  stages {
    stage('Validate Parameters') {
      steps {
        script {
          // Make sure DOCKER_IMAGE is set correctly from environment variables
          env.DOCKER_IMAGE = "${env.DOCKER_REPO_NAME}/${env.DOCKER_IMAGE_NAME}:${env.DOCKER_TAG}"
          if (!env.DOCKER_IMAGE?.trim()) {
            error "The Docker image name is required but not provided."
          }
          echo "Using Docker image: ${env.DOCKER_IMAGE}"  // Debugging line
        }
      }
    }

    stage('Pull Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
          echo "Logging into Docker Hub..."  // Debugging line
          sh """
            docker logout || true  # Ensure no old sessions interfere
            echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io
            echo "Pulling Docker image: ${env.DOCKER_IMAGE}"  // Debugging line
            docker pull ${env.DOCKER_IMAGE}
          """
        }
      }
    }

    stage('Test') {
      steps {
        echo "Running tests on Docker image: ${env.DOCKER_IMAGE}"  // Debugging line
        sh "docker run --rm ${env.DOCKER_IMAGE} python -m pytest app/tests/"
      }
    }

    stage('Run') {
      steps {
        echo "Running container from image: ${env.DOCKER_IMAGE}"  // Debugging line
        sh "docker run -d --name my-flask-app -p 5000:5000 ${env.DOCKER_IMAGE}"
      }
    }
  }

  post {
    always {
      echo "Logging out of Docker..."  // Debugging line
      sh 'docker logout || true'
      echo "Removing any running containers..."  // Debugging line
      sh 'docker ps -q --filter "name=my-flask-app" | xargs --no-run-if-empty docker rm -f || true'
    }
  }
}

