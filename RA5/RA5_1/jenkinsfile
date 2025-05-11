// Jenkinsfile

pipeline {
    agent any

    triggers {
        pollSCM('* * * * *') // Verifica el repositorio cada minuto (puedes cambiarlo)
    }

    stages {
        stage('Clonar repositorio') {
            steps {
                git url: 'https://github.com/migvivcam/PPS-10197785/blob/main/RA5/RA5_1/'
            }
        }

        stage('Instalar dependencias') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
            }
        }

        stage('Pruebas unitarias') {
            steps {
                sh '. venv/bin/activate && python -m unittest test_calculator.py'
            }
        }
    }

    post {
        success {
            echo 'Pruebas completadas con éxito.'
        }
        failure {
            echo 'Error en alguna etapa de la canalización.'
        }
    }
}
