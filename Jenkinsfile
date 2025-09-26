// File: Jenkinsfile

pipeline {
    agent any

    stages {
        // This stage block was missing
        stage('Deploy via SSH to Local PC') {
            steps {
                sshagent(credentials: ['remote-host-creds']) { // Or whatever your final credential ID is
                    script {
                        def remoteUser = "juan"
                        def remoteHost = "192.168.1.2"

                        sh "ssh-keyscan ${remoteHost} >> ~/.ssh/known_hosts"

                        // The deployment script
                        sh """
                            ssh ${remoteUser}@${remoteHost} '
                                # The target directory on your PC for the project
                                # THIS LINE IS NOW CORRECT BASH SYNTAX
                                projectDir="/home/juan/project"

                                if [ -d \${projectDir}/.git ]; then
                                    echo "--- Directory exists, pulling changes ---"
                                    cd \${projectDir} && git pull;
                                else
                                    echo "--- Directory does not exist, cloning repository ---"
                                    mkdir -p \${projectDir} && git clone https://github.com/juanignaciocalle/interview_system \${projectDir};
                                fi
                            '
                        """
                    }
                }
            }
        }
    }
}