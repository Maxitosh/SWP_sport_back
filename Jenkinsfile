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
        sh '''docker-compose -f compose/docker-compose-test.yml build
docker-compose -f compose/docker-compose-test.yml up -d
sleep 3
docker-compose -f compose/docker-compose-test.yml exec -T adminpanel python manage.py makemigrations
docker-compose -f compose/docker-compose-test.yml exec -T adminpanel python manage.py migrate
docker-compose -f compose/docker-compose-test.yml exec -T adminpanel pytest'''
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
