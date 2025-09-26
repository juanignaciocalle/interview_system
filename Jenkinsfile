// File: Jenkinsfile

pipeline {
    agent any

    stages {
        // This stage block was missing
        stage('Deploy via SSH to Local PC') {
            steps {
                // Use the credentials you created with the ID 'remote-host-creds'
                sshagent(credentials: ['remote-host-creds']) {
                    script {
                        // Your specific user and host details
                        def remoteUser = "juan"
                        // IMPORTANT: Double-check this is still your correct IP address!
                        def remoteHost = "192.168.1.15"

                        // Add your PC's SSH key fingerprint to known_hosts
                        sh "ssh-keyscan ${remoteHost} >> ~/.ssh/known_hosts"

                        // The deployment script
                        sh """
                            ssh ${remoteUser}@${remoteHost} '
                                # The target directory on your PC for the project
                                def projectDir = "/home/juan/project"

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