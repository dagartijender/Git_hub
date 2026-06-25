#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 2 ]]; then
  echo "Usage: $0 <organization-url> <project-name>" >&2
  echo "Example: $0 https://dev.azure.com/contoso Enterprise-Microservices" >&2
  exit 2
fi

organization_url="$1"
project_name="$2"

required_commands=(az git)
for command_name in "${required_commands[@]}"; do
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "Required command is not installed: ${command_name}" >&2
    exit 1
  fi
done

if ! az extension show --name azure-devops >/dev/null 2>&1; then
  echo "Install the Azure DevOps CLI extension first:" >&2
  echo "  az extension add --name azure-devops" >&2
  exit 1
fi

az devops configure --defaults \
  organization="${organization_url}" \
  project="${project_name}"

if ! az devops project show \
  --organization "${organization_url}" \
  --project "${project_name}" >/dev/null 2>&1; then
  az devops project create \
    --organization "${organization_url}" \
    --name "${project_name}" \
    --description "Enterprise microservices with central CI/CD templates and GitOps" \
    --source-control git \
    --visibility private
fi

repositories=(
  central-pipeline-templates
  platform-infra
  ai-devops-assistant
  payments-api
  orders-api
  customer-api
  platform-gitops
)

for repository in "${repositories[@]}"; do
  if az repos show \
    --organization "${organization_url}" \
    --project "${project_name}" \
    --repository "${repository}" >/dev/null 2>&1; then
    echo "Repository already exists: ${repository}"
    continue
  fi

  az repos create \
    --organization "${organization_url}" \
    --project "${project_name}" \
    --name "${repository}" >/dev/null
  echo "Created repository: ${repository}"
done

echo
echo "Azure DevOps project is ready: ${project_name}"
echo "Next: create service connections and the enterprise-cicd-secrets / enterprise-infra-secrets variable groups."
