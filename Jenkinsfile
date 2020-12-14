standardShellPipeline {
  credentials = [
    string(credentialsId:'SLACK_WEBHOOK',variable: 'SLACK_WEBHOOK'),
    string(credentialsId:'SLACK_WEBHOOK_LIGHTHOUSE',variable: 'SLACK_WEBHOOK_LIGHTHOUSE')
  ],
  dockerFile = "docker/Dockerfile.build",
  slackDestinations = [
    'api-claims-attributes-jenkins@${env.SLACK_WEBHOOK_LIGHTHOUSE}',
    'health_apis_jenkins@${env.SLACK_WEBHOOK}'
  ]
}
