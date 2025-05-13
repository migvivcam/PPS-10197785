pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clona el repositorio en la rama main
                git branch: 'main', url: 'https://github.com/migvivcam/calculadora.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install pytest
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest test_calculator.py
                '''
            }
        }
    }

    post {
        failure {
            echo 'La ejecución de los tests falló.'
        }
        success {
            echo 'Todos los tests pasaron correctamente.'
        }
    }
}
