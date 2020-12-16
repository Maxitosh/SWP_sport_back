pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'Building..'
      }
    }

    stage('Test') {
      agent {
        docker {
          image 'docker/compose'
        }

      }
      steps {
        echo 'Testing..'
        sh '''export COMPOSE_INTERACTIVE_NO_CLI=1
docker-compose -f compose/docker-compose-test.yml build
docker-compose -f compose/docker-compose-test.yml up -d
sleep 3
docker-compose -f compose/docker-compose-test.yml exec adminpanel python manage.py makemigrations
docker-compose -f compose/docker-compose-test.yml exec adminpanel python manage.py migrate
docker-compose -f compose/docker-compose-test.yml exec adminpanel pytest'''
      }
    }

    stage('Deploy') {
      steps {
        echo 'Deploying....'
      }
    }

  }
}