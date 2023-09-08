node {
    def workspaceDir = pwd()
    // Define the directory to store Allure results and report
    def allureResultsDir = "${workspaceDir}/allure-results"
    def allureReportDir = "${workspaceDir}/allure-report"

    // Clean the Allure report and results directory if it exists
    sh "rm -rf ${allureResultsDir}"
    sh "rm -rf ${allureReportDir}"
    
    properties([parameters(
                [booleanParam(defaultValue: true, description: 'Check the box if voyage active', name: 'isActive'), 
                choice(choices: ['2022', '2023', '2024'], description: 'select the year', name: 'date'), 
                string(defaultValue: '8', description: 'enter no of res', name: 'no_of_res'),
                string(defaultValue: 'dev', description: 'enter stage name', name: 'stage'),
                ])])
              
    def parallelStages = [:]
        stage('SCM') {
            git branch: 'main', url: 'https://github.com/rmohit011/dxp_e2e_automation.git'
        }
      parallelStages['ExecutePython'] = {
        stage('ExecutePython') {
            docker.image('python:3.9.18').inside {
            echo "pass"
            echo "${params.no_of_res}"
            echo "${params.isActive}"
            echo "${params.date}"
            sh "python test_agrs.py ${params.no_of_res} ${params.isActive} ${params.date}"
        }
        }
      }
      parallelStages['ExecutePytest'] = {
        stage('ExecutePytest') {
        docker.image('qnib/pytest:latest').inside {
            echo "${params.stage}"
            sh "pytest test_pyt.py"
            sh "pytest test_cml.py --name=${params.stage}"
        }
    }
      }
    parallel parallelStages
    stage('Test and Generate Allure Results') {
        docker.image('qnib/pytest:latest').inside {
           sh 'virtualenv myenv'

    

            sh '. myenv/bin/activate'
           
            sh 'apt-get update && apt-get install -y openjdk-11-jre && \'
    'apt-get clean && \'
    'rm -rf /var/lib/apt/lists/* && \'
    'wget -O allure.zip https://github.com/allure-framework/allure2/releases/download/2.14.0/allure-2.14.0.zip && \'
    'unzip allure.zip && \'
    'rm allure.zip && \'
    'mv allure-2.14.0 /opt/allure && \'
    'ln -s /opt/allure/bin/allure /usr/bin/allure'


    sh 'pip install allure-pytest pytest'

            sh 'pip install --upgrade pip'
           sh 'pip install allure-pytest'
        // Replace with your test execution commands
        sh 'pytest --alluredir=${allureResultsDir}' // For example, if you're using pytest
    }
    }
    // Generate the Allure report
    stage('Generate Allure Report') {
        docker.image('qnib/pytest:latest').inside {
        // Generate the Allure report from the results
        sh "allure generate ${allureResultsDir} -o ${allureReportDir}"

        // Archive the Allure report so that it can be accessed in Jenkins
        archiveArtifacts artifacts: "${allureReportDir}/*", allowEmptyArchive: true
    }
    }

    // Publish Allure report using the Allure Jenkins Plugin (optional)
    stage('Publish Allure Report') {
        allure([
            includeProperties: false,
            jdk: '',
            properties: [],
            reportBuildPolicy: 'ALWAYS',
            results: [[path: allureResultsDir]],
        ])
    }

}


