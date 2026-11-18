pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        APP_NAME        = 'devops-deployment-monitor'
        REPO_URL        = 'https://github.com/Dharshan-18/python-devops-cicd.git'
        VENV_DIR        = '.venv'
        APP_PORT        = '5000'
        CONTAINER_NAME  = 'devops-deployment-monitor'
        // Set these when pushing to a container registry (e.g. Docker Hub / GHCR):
        DOCKER_REGISTRY = ''
        DOCKER_CREDS_ID = ''
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_SHORT_SHA = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.IMAGE_REPO = env.DOCKER_REGISTRY?.trim()
                        ? "${env.DOCKER_REGISTRY.trim()}/${env.APP_NAME}"
                        : "${env.APP_NAME}"
                    env.IMAGE_TAG = "${env.GIT_SHORT_SHA}"
                }
            }
        }

        stage('Setup & Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest flake8
                '''
            }
        }

        stage('Lint & App Verification') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    flake8 . --exclude=${VENV_DIR},__pycache__,.git --max-line-length=120
                    python -c "from wsgi import application; assert application is not None"
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    mkdir -p test-results
                    pytest --junitxml=test-results/results.xml || [ $? -eq 5 ]
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t ${IMAGE_REPO}:${IMAGE_TAG} -t ${IMAGE_REPO}:latest .
                '''
            }
        }

        stage('Docker Push') {
            when {
                allOf {
                    expression { return env.DOCKER_REGISTRY?.trim() && env.DOCKER_CREDS_ID?.trim() }
                    branch 'main'
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CREDS_ID}",
                    usernameVariable: 'REGISTRY_USER',
                    passwordVariable: 'REGISTRY_PASS'
                )]) {
                    sh '''
                        echo "${REGISTRY_PASS}" | docker login ${DOCKER_REGISTRY%%/*} -u "${REGISTRY_USER}" --password-stdin
                        docker push ${IMAGE_REPO}:${IMAGE_TAG}
                        docker push ${IMAGE_REPO}:latest
                        docker logout ${DOCKER_REGISTRY%%/*}
                    '''
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        --restart unless-stopped \
                        -p ${APP_PORT}:5000 \
                        -e APP_NAME="DevOps Deployment Monitor" \
                        -e APP_VERSION="${IMAGE_TAG}" \
                        -e ENVIRONMENT="Production" \
                        -e FLASK_DEBUG="false" \
                        -e HOST="0.0.0.0" \
                        -e PORT="5000" \
                        -e LOG_LEVEL="INFO" \
                        ${IMAGE_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Health Check') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    for i in $(seq 1 10); do
                        if curl -fsS http://127.0.0.1:${APP_PORT}/health; then
                            echo ""
                            echo "Health check passed."
                            exit 0
                        fi
                        echo "Waiting for app to become healthy (attempt $i/10)..."
                        sleep 2
                    done
                    echo "Health check failed after 10 attempts."
                    docker logs ${CONTAINER_NAME} || true
                    exit 1
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'test-results/*.xml'
            cleanWs()
        }
        success {
            echo "Pipeline succeeded for ${APP_NAME} (${IMAGE_TAG})."
        }
        failure {
            echo "Pipeline failed for ${APP_NAME} (${IMAGE_TAG}). Check console output."
        }
    }
}
