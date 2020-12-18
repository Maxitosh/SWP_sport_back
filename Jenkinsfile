pipeline {
  agent any
  stages {
    stage('Test') {
      agent {
        docker {
          image 'docker/compose'
        }

      }
      steps {
        echo 'Testing..'
        sh 'docker-compose -f compose/docker-compose-test.yml build'
        sh 'docker-compose -f compose/docker-compose-test.yml up -d'
        sh 'sleep 3'
        sh 'docker-compose -f compose/docker-compose-test.yml exec -T adminpanel python manage.py makemigrations'
        sh 'docker-compose -f compose/docker-compose-test.yml exec -T adminpanel python manage.py migrate'
        sh 'docker-compose -f compose/docker-compose-test.yml exec -T adminpanel pytest'
      }
      post {
        cleanup {
          echo 'Cleanup...'
          //sh 'docker-compose -f compose/docker-compose-test.yml down'  
        }
      }
    }

    stage('Build') {
      environment {
        PYTHON_VERSION = credentials('python-version')
      }
      steps {
        echo 'Building..'
        script {
          dockerInstanceDjango = docker.build("winnerokay/sna-app", '--build-arg PYTHON_VERSION=$PYTHON_VERSION ./adminpage')
        }
      }
    }
    
    stage('Migrate'){
      steps {
        echo 'Making migrations to the db...' 
      }
    }
    
    stage('Push to registry') {
      environment {
        registryCredentialSet = 'dockerhub'
      }
      steps {
        echo 'Publishing....'
        script{
          docker.withRegistry('', registryCredentialSet){
            dockerInstanceDjango.push("${env.BUILD_NUMBER}")
            dockerInstanceDjango.push("latest")
          }
        }
      }
    }
    
    stage('Deploy'){
      steps {
        echo 'Deploying...'
      }
    }
  }
}
