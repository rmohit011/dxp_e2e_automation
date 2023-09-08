node {
    properties([parameters(
                [booleanParam(defaultValue: true, description: 'Check the box if voyage active', name: 'isActive'), 
                choice(choices: ['2022', '2023', '2024'], description: 'select the year', name: 'date'), 
                string(defaultValue: '8', description: 'enter no of res', name: 'no_of_res'),
                string(defaultValue: 'dev', description: 'enter stage name', name: 'stage'),
                ])])
    properties([
        pipelineTriggers([
            [$class: 'SCMTrigger', scmpoll_spec: 'H/15 * * * *']
        ])
    ])
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
}

