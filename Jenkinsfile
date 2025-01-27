#pipeline {
  #agent any

  #stages {
    #stage('Build') {
      #steps {
       # sh 'docker build -t my-flask-app .'
      #  sh 'docker tag my-flask-app $DOCKER_BFLASK_IMAGE'
     # }
    #}
    #stage('Test') {
      #steps {
      #  sh 'docker run my-flask-app python -m pytest app/tests/'
     # }
    #}
    #stage('Deploy') {
      #steps {
        #withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
       #   sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io"
      #    sh 'docker push $DOCKER_BFLASK_IMAGE'
     #   }
    #  }
   # }
  #}
  #post {
    #always {
   #   sh 'docker logout'
  #  }
 # }
#}

pipeline {
  agent any

  parameters {
    string(name: 'DOCKER_IMAGE', defaultValue: '', description: 'Enter the full Docker image name (e.g., my-repo/my-flask-app:tag)')
  }

  stages {
    stage('Validate Parameters') {
      steps {
        script {
          if (!params.DOCKER_IMAGE?.trim()) {
            error "The parameter 'DOCKER_IMAGE' is required but not provided."
          }
        }
      }
    }
    stage('Pull Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: "${DOCKER_REGISTRY_CREDS}", passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
          sh """
            echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin docker.io
            docker pull ${params.DOCKER_IMAGE}
          """
        }
      }
    }
    stage('Test') {
      steps {
        sh "docker run --rm ${params.DOCKER_IMAGE} python -m pytest app/tests/"
      }
    }
    stage('Run') {
      steps {
        sh "docker run -d --name my-flask-app -p 5000:5000 ${params.DOCKER_IMAGE}"
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
      sh 'docker ps -q --filter "name=my-flask-app" | xargs --no-run-if-empty docker rm -f || true'
    }
  }
}
  
