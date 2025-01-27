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

  environment {
    DOCKER_IMAGE = 'siddamjayachandra/todo:latest'
    CONTAINER_PORT = '5000'
    HOST_PORT = '5000'
  }

  stages {
    stage('Build') {
      steps {
        sh 'docker build -t $DOCKER_IMAGE .'
        sh 'docker push $DOCKER_IMAGE'
      }
    }

    stage('Test') {
      steps {
        sh 'docker run $DOCKER_IMAGE python -m pytest app/tests/'
      }
    }

    stage('Deploy') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
          sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
          sh 'docker pull $DOCKER_IMAGE'

          // Stop any running container
          sh 'docker ps -q --filter "name=my-todo-app" | xargs -r docker stop'
          sh 'docker ps -a -q --filter "name=my-todo-app" | xargs -r docker rm'

          // Run the container
          sh 'docker run -d --name my-todo-app -p $HOST_PORT:$CONTAINER_PORT $DOCKER_IMAGE'
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout'
    }
  }
}
