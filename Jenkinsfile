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
    
    try {          
    def parallelStages = [:]
        stage('SCM') {
            git branch: 'main', url: 'https://github.com/rmohit011/dxp_e2e_automation.git'
            sh "docker build -t jenkins-venv:1.0 ."
        }
      parallelStages['ExecutePython'] = {
        stage('ExecutePython') {
            docker.image('jenkins-venv:1.0'){
            echo "${params.no_of_res}"
            echo "${params.isActive}"
            echo "${params.date}"
            sh "python test_agrs.py ${params.no_of_res} ${params.isActive} ${params.date}"
            sh "python grid.py"
        }
        }
      }
      parallelStages['ExecutePytest'] = {
        stage('ExecutePytest and Generate allure result') {
        docker.image('jenkins-venv:1.0').inside {
            echo "${params.stage}"
            sh "pytest test_pyt.py"
            sh "pytest --name=${params.stage} --alluredir=${allureResultsDir}"
        }
    }
      }
    parallel parallelStages
    }
    catch (Exception e) {
        currentBuild.result = 'FAILURE'
        echo "One or more stages have failed, but the pipeline continues..."
    } finally {
    
    // Generate the Allure report
    stage('Generate Allure Report') {
        docker.image('jenkins-venv:1.0').inside {
        // Generate the Allure report from the results
        sh "allure generate ${allureResultsDir} -o ${allureReportDir}"

        // Archive the Allure report so that it can be accessed in Jenkins
        archiveArtifacts artifacts: "allure-report/*", allowEmptyArchive: true
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

}
