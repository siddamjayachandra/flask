pipeline {
  agent any

  parameters {
    string(name: 'DOCKER_IMAGE', defaultValue: 'my-repo/my-flask-app:latest', description: 'Enter the full Docker image name (e.g., my-repo/my-flask-app:tag)')
  }

  stages {
    stage('Validate Parameters') {
      steps {
        script {
          // Check if the DOCKER_IMAGE parameter is empty
          if (!params.DOCKER_IMAGE?.trim()) {
            error "The parameter 'DOCKER_IMAGE' is required but not provided."
          }
          echo "DOCKER_IMAGE: ${params.DOCKER_IMAGE}" // Debugging line
        }
      }
    }

    stage('Pull Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
          echo "Logging into Docker Hub..."  // Debugging line
          sh """
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
        sh "docker run -d --name my-flask-app -p 5000:5000 ${params.DOCKER_IMAGE}"
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

