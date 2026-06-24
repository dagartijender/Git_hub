# Terraform Infrastructure

This folder provisions the Azure foundation for the GitOps platform:

- Resource group
- Azure Container Registry
- AKS cluster
- Log Analytics workspace
- AKS `AcrPull` access to ACR

## State Backend

The Terraform pipeline expects an Azure Storage backend. Create it once before
running the pipeline, then store these values in the `enterprise-infra-secrets`
variable group:

```text
tfStateResourceGroup=<state-resource-group>
tfStateStorageAccount=<state-storage-account>
tfStateContainer=tfstate
azureServiceConnection=sc-azure-terraform-enterprise
```

Each environment uses a separate state key:

```text
gitops-platform/dev.tfstate
gitops-platform/staging.tfstate
gitops-platform/prod.tfstate
```

## Local Commands

```bash
terraform init \
  -backend-config="resource_group_name=<state-resource-group>" \
  -backend-config="storage_account_name=<state-storage-account>" \
  -backend-config="container_name=tfstate" \
  -backend-config="key=gitops-platform/dev.tfstate"

terraform plan -var-file=environments/dev.tfvars
```

Production changes should go through pull request review and Azure DevOps
environment approval before `apply`.

