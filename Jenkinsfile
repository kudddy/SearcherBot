pipeline {
    agent any
    environment {
        DISABLE_AUTH = 'true'
        GOOGLE_PROJECT_ID = 'velvety-harbor-284611'
        GOOGLE_SERVICE_ACCOUNT_KEY = credentials('service_acc');
        GOOGLE_APP_NAME = 'telebot'
    }
    stages {
        stage('Logging in Docker and gcloud') {
            steps {
                echo 'Starting to build docker image'

                script {
                    echo 'log in gcloud'
                    sh """
                    /gcloud/google-cloud-sdk/bin/gcloud auth activate-service-account --key-file ${GOOGLE_SERVICE_ACCOUNT_KEY};
                    /gcloud/google-cloud-sdk/bin/gcloud config set project ${GOOGLE_PROJECT_ID};
                    /gcloud/google-cloud-sdk/bin/gcloud components install docker-credential-gcr;
                    echo "After authentication gcloud";
                    export PATH=/gcloud/google-cloud-sdk/bin/:$PATH;
                    /gcloud/google-cloud-sdk/bin/gcloud auth configure-docker
                    cat ${GOOGLE_SERVICE_ACCOUNT_KEY} | docker login https://gcr.io -u _json_key --password-stdin
                    """
                }
            }
        }
        stage('Build image') {
            steps {
                echo 'Starting to build docker image'

                script {
                    echo 'log in gcloud'
                    def customImage = docker.build("gcr.io/${GOOGLE_PROJECT_ID}/${GOOGLE_APP_NAME}")

                    customImage.push()
                    echo 'log OK'
                    sh """
                    /gcloud/google-cloud-sdk/bin/gcloud app deploy --image-url gcr.io/${GOOGLE_PROJECT_ID}/${GOOGLE_APP_NAME}
                    """
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Start deploy'

                script {
                    sh """
                    /gcloud/google-cloud-sdk/bin/gcloud app deploy --image-url gcr.io/${GOOGLE_PROJECT_ID}/${GOOGLE_APP_NAME}
                    """
                }
            }
        }
    }
}