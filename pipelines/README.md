# Central Azure DevOps Pipeline Templates

Each microservice pipeline includes the central stage templates directly. The
pipeline remains easy to read while the implementation stays centrally
governed.

## Pipeline Structure

```yaml
variables:
  - group: enterprise-cicd-secrets
  - name: imageTag
    value: $(Build.BuildId)

stages:
  - template: pipelines/templates/stages/build.yml@centralTemplates
    parameters:
      serviceName: payments-api
      buildSteps: []

  - template: pipelines/templates/stages/publish.yml@centralTemplates
    parameters:
      serviceName: payments-api
      artifactPath: src
      artifactName: drop

  - template: pipelines/templates/stages/security.yml@centralTemplates
    parameters:
      serviceName: payments-api
      artifactName: drop

  - template: pipelines/templates/stages/container.yml@centralTemplates
    parameters:
      dockerfile: Dockerfile
      imageRepository: payments-api
      imageTag: $(Build.BuildId)

  - template: pipelines/templates/stages/gitops.yml@centralTemplates
    parameters:
      imageTag: $(Build.BuildId)
      gitopsValuesFile: apps/payments-api/environments/dev/values.yaml
```

## Standard Lifecycle

### Application Delivery

1. Build and test the microservice.
2. Run secret scanning and SonarQube.
3. Package and publish the `drop` pipeline artifact.
4. Run Black Duck and Veracode.
5. Call the microservice's Dockerfile.
6. Push the image tagged with `$(Build.BuildId)` to ACR.
7. Commit the same build ID to the GitOps values file.
8. Let ArgoCD deploy the Helm release to AKS.

### Infrastructure Delivery

1. Validate Terraform formatting and configuration.
2. Initialize Terraform against the Azure Storage state backend.
3. Create and publish a Terraform plan artifact.
4. Apply the reviewed plan artifact from `main`.
5. Protect higher environments with Azure DevOps environment approvals.

## Central Templates

| Template | Responsibility |
|---|---|
| `stages/build.yml` | Runtime, build, tests, SonarQube, secret scan |
| `stages/publish.yml` | Package and publish the `drop` pipeline artifact |
| `stages/security.yml` | Black Duck and Veracode |
| `stages/container.yml` | Push stage for Dockerfile build and ACR push |
| `stages/gitops.yml` | Helm values image-tag update |
| `stages/terraform-validate.yml` | Terraform format and validate |
| `stages/terraform-plan.yml` | Terraform init, plan, and plan artifact publish |
| `stages/terraform-apply.yml` | Approved Terraform apply from published plan |
| `steps/*.yml` | Reusable task-level implementation |

## External Repository Consumption

```yaml
resources:
  repositories:
    - repository: centralTemplates
      type: git
      name: PlatformEngineering/central-pipeline-templates
      ref: refs/tags/v1.0.0
```

Pin production consumers to a version tag. Protect and review changes in the
central template repository.
