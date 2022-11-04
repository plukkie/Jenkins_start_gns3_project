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

    	stage('Show host versions') {
      		steps {
			echo 'Get python3 versions:'
        		sh 'python3 --version'
			sh 'pip3 list'
      		}
    	}
/*
    	stage('Stop GNS3 Stage PROD') {
      		steps {
			echo 'Request API call to GNS3 server to stop Prod fabric.'
        		sh 'python3 -u startcicd.py stopgns3 prodstage'
			sleep( time: 3 )
      		}
	}
*/
    	stage('Stage Dev: Provision GNS3 Dev network') {
		
		environment {
			LS = "${sh(script:'python3 -u startcicd.py startgns3 teststage | grep "proceed"', returnStdout: true).trim()}"
    		}
      		
		steps {
			script {
				echo "${env.LS}" 
				if (env.LS == 'proceed = True') {
					echo 'Network already provisioned. Proceed to Stage Dev: Configure Dev network'
                                        sleep( time: 2 )
                                }
				else {
					//GNS3 API call to start Network has just been done by startcicd.py script
					echo 'Dev network is being provisioned. This can take ~3 mins'
        				//sh 'python3 -u startcicd.py startgns3 teststage'
					echo 'Waiting for systems te become active'
					sleep( time: 180 )
                                }
			}
      		}
	}

	stage("Stage Dev: Configure Dev network") {
		environment {
			LS = "${sh(script:'python3 -u startcicd.py launchawx teststage deploy | grep "proceed"', returnStdout: true).trim()}"
    		}
                            
		steps {
			script {
				echo 'Waiting till network configuration has finished. This can take ~15 minutes.'
				echo "${env.LS}"
				if (env.LS == 'proceed = "True"') {
					sleep( time: 10 )
            				echo 'Proceed to Stage Dev fase testing...'
        			} else {
            				error ("There were failures in the job template execution. Pipeline stops here.")
        			}
			}
		}
        }
	  
	stage("Stage Dev: Run connectivity Tests") {
		environment {
			LS = "${sh(script:'python3 -u startcicd.py launchawx teststage test | grep "proceed"', returnStdout: true).trim()}"
    		}
            
		steps {
			script {
				echo 'Waiting till network ping tests have finished. This can take some minutes.'
				echo "${env.LS}"
				if (env.LS == 'proceed = "True"') {
					echo 'All pingtests succeeded.'
					sleep( time: 2 )
					/*
					echo 'Will decommision Dev network to spare GNS3 resources...'
					sleep( time: 2 )
					sh 'python3 -u startcicd.py stopgns3 teststage'
					*/
            				echo 'Proceed to Stage Prod fase Provision'
					sleep( time: 3 )
        			} else {
            				error ("There were failures in the job template execution. Pipeline stops here.")
        			}
			}
		}
        }
    	
	stage('Stage Prod: Provision GNS3 prod network') {
		
		environment {
			LS = "${sh(script:'python3 -u startcicd.py startgns3 prodstage | grep "proceed"', returnStdout: true).trim()}"
    		}
      		
		steps {
			script {
				echo "${env.LS}" 
				if (env.LS == 'proceed = "True"') {
					echo 'Network already provisioned. Proceed to Stage Prod: Configure Prod network'
                                        sleep( time: 2 )
                                }
				else {
					//GNS3 API call to start Network has just been done by startcicd.py script
					echo 'Prod network is being provisioned. This can take ~3 mins'
					echo 'Waiting for systems te become active'
					sleep( time: 180 )
                                }
			}
      		}
	}

	stage("Stage Prod: Configure Prod network") {
		environment {
			LS = "${sh(script:'python3 -u startcicd.py launchawx prodstage deploy | grep "proceed"', returnStdout: true).trim()}"
    		}
                            
		steps {
			script {
				echo 'Waiting till network deployment has finished. This can take ~15 minutes.'
				echo "${env.LS}"
				if (env.LS == 'proceed = "True"') {
					sleep( time: 10 )
            				echo 'Proceed to Stage Pod fase Ping Tests'
        			} else {
            				error ("There were failures in the job template execution. Pipeline stops here.")
        			}
			}
		}
        }

	stage("Stage Prod: Run connectivity Tests") {
		environment {
			LS = "${sh(script:'python3 -u startcicd.py launchawx prodstage test | grep "proceed"', returnStdout: true).trim()}"
    		}
            
		steps {
			script {
				echo 'Waiting till network ping tests have finished. This can take some minutes.'
				echo "${env.LS}"
				if (env.LS == 'proceed = "True"') {
					echo 'All pingtests succeeded.'
					sleep( time: 2 )
            				echo 'The production network runs fine with the new changes :-)'
					sleep( time: 2 )
        			} else {
            				error ("There were failures in the job template execution. Pipeline stops here.")
        			}
			}
		}
        }

  }
}

