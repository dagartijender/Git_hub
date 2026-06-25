# AI DevOps Assistant

This project demonstrates an AI-assisted DevOps triage workflow for Azure
DevOps, ACR, Terraform, AKS, Helm, ArgoCD, SonarQube, Black Duck, Veracode, and
secret scanning.

The first implementation is deterministic and pipeline-safe: it classifies
pipeline logs using curated DevOps failure rules, confidence scoring, and
recommended actions. A future LLM integration can use the same report model and
prompt assets without changing the pipeline contract.

## Use Cases

- Summarize failed Azure DevOps pipeline logs.
- Classify failures by area: security, code quality, Terraform, container,
  registry, Kubernetes, or GitOps.
- Recommend owners and priorities for incident follow-up.
- Publish triage output as a build artifact.
- Feed triage summaries into pull request comments, incident tickets, or chat
  notifications.

## Local Usage

```bash
python3 -m ai_devops_assistant.cli ai-devops/examples/failed-pipeline.log
python3 -m ai_devops_assistant.cli ai-devops/examples/failed-pipeline.log --format json
```

## Pipeline

`azure-pipelines-ai-devops.yml` builds and tests the assistant, publishes the
package as a `drop` artifact, runs enterprise security templates, and pushes an
optional container image to ACR using `$(Build.BuildId)`.

## Extension Ideas

- Add Azure OpenAI or OpenAI summarization behind the deterministic report.
- Post Markdown summaries to pull requests.
- Create Azure DevOps work items for repeated failure categories.
- Send high-severity failures to Teams or Slack.
- Store anonymized failure patterns for trend dashboards.

