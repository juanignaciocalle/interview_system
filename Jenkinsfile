// File: Jenkinsfile

pipeline {
    agent any

    stages {
        // comment for testing
        // Stage 1: Checkout the code from GitHub
        // This stage is mostly for confirmation, as Jenkins has already
        // checked out the code to find this Jenkinsfile.
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // Stage 2: Deploy the code to the remote host
        stage('Deploy via SSH') {
            steps {
                // Use the credentials you created with the ID 'remote-host-creds'
                sshagent(credentials: ['remote-host-creds']) {
                    script {
                        // 'remote_host' is the service name from docker-compose.yml.
                        // Docker's networking lets Jenkins find it by this name.
                        // This step prevents the pipeline from getting stuck asking
                        // "Are you sure you want to continue connecting (yes/no)?"
                        sh 'ssh-keyscan remote_host >> ~/.ssh/known_hosts'

                        // This is the main command.
                        // It logs into your remote_host container and runs git pull.
                        // The directory was created by the ssh-server/Dockerfile.
                        // NOTE: For the very first run, the 'git pull' will fail
                        // because the directory is empty. A 'git clone' is better for the first time.
                        // A more robust script is shown below.
                        sh '''
                            ssh app-user@remote_host '
                                if [ -d /home/app-user/project/.git ]; then
                                    cd /home/app-user/project && git pull;
                                else
                                    git clone https://github.com/juanignaciocalle/interview_system /home/app-user/project;
                                fi
                            '
                        '''
                    }
                }
            }
        }
    }
}