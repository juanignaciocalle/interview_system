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
                        // FIX: Create the .ssh directory if it doesn't exist
                        sh 'mkdir -p ~/.ssh'

                        // This command will now succeed because the directory exists
                        sh 'ssh-keyscan remote_host >> ~/.ssh/known_hosts'

                        // The rest of your script remains the same
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