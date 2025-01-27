pipeline {
  agent any

  parameters {
    string(name: 'DOCKER_IMAGE', defaultValue: 'siddamjayachandra/todo:latest', description: 'Enter the full Docker image name (e.g., my-repo/my-flask-app:tag)')
  }

  stages {
    stage('Validate Parameters') {
      steps {
        script {
          // Check if the DOCKER_IMAGE parameter is provided
          if (!params.DOCKER_IMAGE?.trim()) {
            error "The parameter 'DOCKER_IMAGE' is required but not provided."
          }
          echo "Using Docker image: ${params.DOCKER_IMAGE}"  // Debugging line
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
            echo "Pulling Docker image: ${params.DOCKER_IMAGE}"  // Debugging line
            docker pull ${params.DOCKER_IMAGE}
          """
        }
      }
    }

    stage('Test') {
      steps {
        echo "Running tests on Docker image: ${params.DOCKER_IMAGE}"  // Debugging line
        sh "docker run --rm ${params.DOCKER_IMAGE} python -m pytest app/tests/"
      }
    }

    stage('Run') {
      steps {
        echo "Running container from image: ${params.DOCKER_IMAGE}"  // Debugging line
        sh "docker run -p 5000:5000 ${params.DOCKER_IMAGE}"
      }
    }
  }

  post {
    always {
      echo "Logging out of Docker..."  // Debugging line
      sh 'docker logout || true'
      echo "Removing any running containers..."  // Debugging line
      sh 'docker ps -q --filter "name=siddamjayachandra/todo:latest" | xargs --no-run-if-empty docker rm -f || true'
    }
  }
}

