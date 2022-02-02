library "JenkinsLib"

e2eRepo = 'dxp-e2e-automation'
e2eBranch = common.getGitBranch()
libRepo = 'automation-lib'
libBranch = 'master'
totalRetries = 1
e2eGuests = 4

parameters = [
    string(defaultValue: 'https://qa1-sagar.decurtis.cloud', description: "Ship Link", name: 'shipLink', trim: true),
    string(defaultValue: 'https://qa1-shore.decurtis.cloud', description: "Shore Link", name: 'shoreLink', trim: true),
]

if (JOB_BASE_NAME.toLowerCase().contains('-branch')) {
    parameters += [
        string(defaultValue: 'master', description: "E2E Branch", name: 'E2EBranch', trim: true),
        string(defaultValue: 'master', description: "Lib Branch", name: 'LibBranch', trim: true),
    ]
}

properties([
    buildDiscarder(logRotator(daysToKeepStr: '5', numToKeepStr: '500')),
    azureAdAuthorizationMatrix(common.azurePermissions([users: [], build: true, read: true, cancel: true])),
    parameters(parameters)
])

testBed = e2e.getTestBed(params.shoreLink)
env.TEAMS_CHANNEL = e2e.getChannelName(params.shipLink)

currentBuild.displayName = "$BUILD_NUMBER - ${testBed.toUpperCase()}"

userTriggered = common.getBuildUser()['email']
mentions = [userTriggered,]
description = [userTriggered.toUpperCase()]

if (params.containsKey('E2EBranch')) {
    if (params.E2EBranch != 'master') {
        description.add("E2E: $params.E2EBranch")
    }
    e2eBranch = params.E2EBranch
}

if (params.containsKey('LibBranch')) {
    if (params.LibBranch != 'master') {
        description.add("LIB: $params.LibBranch")
    }
    libBranch = params.LibBranch
}

currentBuild.description = description.unique().sort().join(" ")

pod.kubeNode(pod.ReturnContainers()) {
    if (params.containsKey('LibBranch') && libBranch != 'master') {
        libCommit = scmWrapper.gitClone([repoName: libRepo, branch: libBranch, clean: true, folder: true])
        dir (libRepo) {
            script = "git diff ..origin/master --name-only | grep requirements.txt | wc -l"
            count = sh (returnStdout: true, script: script).trim().toInteger()
            if (count > 0) {
                stage('Pip Packages') {
                    sh '''
                        set +x
                        rm -rf ~/e2e-venv
                        python3 -m venv ~/e2e-venv
                        . ~/e2e-venv/bin/activate
                        python3 -m pip install --quiet --no-cache-dir --upgrade pip setuptools wheel pyopenssl
                        python3 -m pip install --quiet --no-cache-dir --requirement $WORKSPACE/automation-lib/requirements.txt
                        deactivate
                    '''
                }
            }
        }
        sh 'rsync -aizrtq $WORKSPACE/automation-lib/decurtis ~/e2e-venv/lib/python3.8/site-packages/'
    }

    if (params.shoreLink.contains('ci.decurtis.cloud')) {
        cluster = 'developer'
    } else if (params.shoreLink.contains('qa1-shore.decurtis.cloud')) {
        cluster = 'developer'
    } else if (params.shoreLink.contains('dc-shore.decurtis.cloud')) {
        cluster = 'developer'
    } else {
        cluster = 'dev'
    }

    e2eCommit = scmWrapper.gitClone([repoName: e2eRepo, branch: e2eBranch, clean: true, folder: true])
    dir(e2eRepo) {
        for (iter = 1; iter <= totalRetries; iter++) {
            pyTestParams = [
                "--ship=$params.shipLink",
                "--shore=$params.shoreLink",
                "--guests=$e2eGuests",
                "--test-rail",
            ]
            stage("Running E2E $iter") {
                try {
                    python.RunPyTest([
                        pyTestParams: pyTestParams, pyTestsPath: 'test_scripts', allureReport: true,
                        reportName: "e2e-report-$iter", timeOut: 90, mentions: mentions, exitFirst: true,
                    ])
                    scmWrapper.StatusUpdate([
                        commit: e2eCommit, repoName: e2eRepo, message: "E2E Passed", status: 'SUCCESSFUL'
                    ])
                    if (params.containsKey('LibBranch') && libBranch != 'master') {
                        scmWrapper.StatusUpdate([
                            commit: libCommit, repoName: libRepo, message: "E2E Passed", status: 'SUCCESSFUL'
                        ])
                    }
                    log.Success("E2E has passed after $iter iterations :)")
                    iter = totalRetries + 1
                } catch (e) {
                    if (iter >= totalRetries) {
                        scmWrapper.StatusUpdate([
                            commit: e2eCommit, repoName: e2eRepo, message: "E2E Failed", status: 'FAILED'
                        ])
                        if (params.containsKey('LibBranch') && libBranch != 'master') {
                            scmWrapper.StatusUpdate([
                                commit: libCommit, repoName: libRepo, message: "E2E Failed", status: 'FAILED'
                            ])
                        }
                        log.Fail("E2E has failed after $totalRetries iterations :( $e.message")
                    } else {
                        unstable(message: "Stage: $STAGE_NAME failed, triggering next one :( $e.message")
                    }
                }
            }
        }
    }
}
