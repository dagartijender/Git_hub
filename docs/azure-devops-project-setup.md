# Azure DevOps Project Setup

## Repositories

Create one Azure DevOps project, for example `Enterprise-Microservices`, with:

| Repository | Responsibility |
|---|---|
| `central-pipeline-templates` | Governed YAML templates |
| `platform-infra` | Terraform for AKS, ACR, and Azure platform resources |
| `payments-api` | Python microservice |
| `orders-api` | Node.js microservice |
| `customer-api` | Java microservice |
| `platform-gitops` | Helm charts and environment values |

The application repositories contain thin pipeline files. The shared
implementation lives only in `central-pipeline-templates`.

After signing in with `az login`, create the project and empty repositories:

```bash
az extension add --name azure-devops
./scripts/bootstrap-azure-devops.sh \
  https://dev.azure.com/<organization> \
  Enterprise-Microservices
```

The script is idempotent: existing projects and repositories are retained.

## Extensions

Install and approve:

- SonarQube Azure DevOps extension
- Veracode Azure DevOps extension

The central template runs a pinned Gitleaks container for pipeline secret
scanning. For native repository alerts and push protection, enable GitHub
Advanced Security for Azure DevOps secret scanning. Black Duck Detect is
launched by the shared template; internally mirror its bootstrap script if
your supply-chain policy requires it.

## Service Connections

Create:

| Name | Type | Scope |
|---|---|---|
| `sc-azure-terraform-enterprise` | Azure Resource Manager | Create and update Azure infrastructure |
| `sc-acr-enterprise` | Docker Registry / ACR | Push images |
| `sc-sonarqube-enterprise` | SonarQube | Analyze projects |
| `sc-veracode-enterprise` | Veracode Platform | Upload and scan |

Expose their names through the shared variable group:

```text
azureServiceConnection=sc-azure-terraform-enterprise
acrServiceConnection=sc-acr-enterprise
sonarServiceConnection=sc-sonarqube-enterprise
veracodeServiceConnection=sc-veracode-enterprise
```

## Variable Group

Create `enterprise-cicd-secrets` and authorize it for approved pipelines:

| Variable | Secret |
|---|---|
| `acrServiceConnection` | No |
| `sonarServiceConnection` | No |
| `veracodeServiceConnection` | No |
| `blackDuckUrl` | No |
| `blackDuckToken` | Yes |
| `gitOpsRepositoryUrl` | No |
| `gitOpsPushToken` | Yes |

Prefer Azure Key Vault-backed variable groups for tokens.

Create `enterprise-infra-secrets` for the Terraform pipeline:

| Variable | Secret |
|---|---|
| `azureServiceConnection` | No |
| `tfStateResourceGroup` | No |
| `tfStateStorageAccount` | No |
| `tfStateContainer` | No |
| `approvalNotifyUsers` | No |
| `approvalApprovers` | No |

If your organization uses self-hosted Azure DevOps agents, pass the pool into
the central stages with `poolName` and optional `poolDemands`. Keep the agent
pools prepared with Docker, Git, Bash, and the language runtimes required by
the microservice build.

## Pipeline Creation

Create one pipeline per microservice and select the service repository's
`azure-pipelines.yml`. Each file imports the central repository, includes the
shared stage templates, and passes only service-specific parameters.

Create one infrastructure pipeline from `azure-pipelines-infra.yml`. It imports
the central Terraform stage templates:

- `TerraformValidate`
- `TerraformPlan`
- `TerraformApproval`
- `TerraformApply`

The `TerraformApproval` stage uses Azure DevOps `ManualValidation` so the plan
artifact is reviewed before apply. Also set approvals on Azure DevOps
environments such as `infra-dev`, `infra-staging`, and `infra-prod` for a
second control layer.

Grant the pipeline's Build Service identity read access to
`central-pipeline-templates`. Grant its GitOps identity contribute permission
only to `platform-gitops`.

## Governance

- Require pull requests and two reviewers for central-template changes.
- Require successful template validation before merge.
- Add required-template approval to service pipelines.
- Tag stable template releases such as `v1.0.0`.
- Restrict production GitOps changes to pull requests and environment
  approvals.
- Do not give CI pipelines AKS credentials.
- Give AKS managed identity `AcrPull`; give CI only ACR push rights.

## Delivery Flow

```mermaid
flowchart LR
    ServiceRepo["Microservice repository"] --> Pipeline["Thin service pipeline"]
    Templates["Central template repository"] --> Pipeline
    Pipeline --> Build["Build stage: tests, SonarQube, secret scan"]
    Build --> Publish["Publish stage: drop artifact"]
    Publish --> Scans["Security stage: Black Duck / Veracode"]
    Scans --> ACR["Push stage: ACR image"]
    ACR --> GitOps["GitOps repository tag update"]
    InfraRepo["Terraform repository"] --> InfraPipeline["Infra pipeline"]
    Templates --> InfraPipeline
    InfraPipeline --> TFPlan["Terraform plan artifact"]
    TFPlan --> Approval["Manual approval"]
    Approval --> TFApply["Approved Terraform apply"]
    TFApply --> AKS
    TFApply --> ACR
    GitOps --> ArgoCD["ArgoCD"]
    ArgoCD --> AKS["AKS Helm release"]
    AKS --> ACR
```
