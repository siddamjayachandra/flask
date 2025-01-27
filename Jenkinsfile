pipeline {
  agent any

  parameters {
    string(name: 'DOCKER_IMAGE', defaultValue: '', description: 'Enter the full Docker image name (e.g., my-repo/my-flask-app:tag)')
    string(name: 'REPO_NAME', defaultValue: 'siddamjayachandra/todo', description: 'Enter your Docker Hub repository name (e.g., my-repo)')
    string(name: 'IMAGE_NAME', defaultValue: 'my-flask-app', description: 'Enter the image name (e.g., my-flask-app)')
    string(name: 'TAG', defaultValue: 'latest', description: 'Enter the image tag (e.g., latest)')
  }

  stages {
    stage('Validate Parameters') {
      steps {
        script {
          // Check if any of the parameters are empty
          if (!params.DOCKER_IMAGE?.trim()) {
            // Construct the DOCKER_IMAGE dynamically using the REPO_NAME, IMAGE_NAME, and TAG parameters
            env.DOCKER_IMAGE = "${params.REPO_NAME}/${params.IMAGE_NAME}:${params.TAG}"
          }
          echo "DOCKER_IMAGE: ${env.DOCKER_IMAGE}"  // Debugging line
        }
      }
    }

    stage('Pull Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
          echo "Logging into Docker Hub..."  // Debugging line
          sh """
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

