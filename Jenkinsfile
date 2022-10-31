pipeline {
  agent any
  stages {
	stage('Build') {
		steps {
			sh 'pip install -r pyrequirements.txt'
			sh 'python3 -m py_compile startcicd.py'
			stash(name: 'compiled-results', includes: '*.py*')
		}
	}

    	stage('version') {
      		steps {
        		sh 'python3 --version'
      		}
    	}

    	stage('start gns3') {
      		steps {
        		sh 'python3 -u startcicd.py startgns3'
			sleep(time: 30)
      		}
	}

	stage('start awx jobtemplate') {
		environment {
                	result = ""
            	}
		steps {
			result = sh('python3 -u startcicd.py launchawx',returnStdout: true)
			echo "result = ${env.result}"
		}
    	}
  }
}

