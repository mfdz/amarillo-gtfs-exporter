pipeline {
    agent any
    environment {
        GITEA_CREDS = credentials('AMARILLO-JENKINS-GITEA-USER')
        TWINE_REPO_URL = "https://git.gerhardt.io/api/packages/amarillo/pypi"
    }
    stages {
        stage('Create virtual environment') {
            steps {
                echo 'Creating virtual environment'
                sh '''python3 -m venv .venv
                . .venv/bin/activate'''
            }
        }
        stage('Installing requirements') {
            steps {
                echo 'Installing packages'
                sh 'python3 -m pip install -r requirements.txt'
                sh 'python3 -m pip install --upgrade build'
                sh 'python3 -m pip install --upgrade twine'
            }
        }
        stage('Build') {
            steps {
                echo 'Building package'
                sh 'python3 -m build'
            }
        }
        stage('Publish package') {
            steps {
                sh 'python3 -m twine upload --skip-existing --verbose --repository-url $TWINE_REPO_URL --username $GITEA_CREDS_USR --password $GITEA_CREDS_PSW ./dist/*'              
            }
        }
    }
}