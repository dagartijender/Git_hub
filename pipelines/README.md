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
      artifactName: drop
      buildSteps: []

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

1. Build and test the microservice.
2. Run secret scanning and SonarQube.
3. Package and publish the `drop` pipeline artifact.
4. Run Black Duck and Veracode.
5. Call the microservice's Dockerfile.
6. Push the image tagged with `$(Build.BuildId)` to ACR.
7. Commit the same build ID to the GitOps values file.
8. Let ArgoCD deploy the Helm release to AKS.

## Central Templates

| Template | Responsibility |
|---|---|
| `stages/build.yml` | Runtime, build, tests, SonarQube, secret scan, artifact |
| `stages/security.yml` | Black Duck and Veracode |
| `stages/container.yml` | Dockerfile build and ACR push |
| `stages/gitops.yml` | Helm values image-tag update |
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
