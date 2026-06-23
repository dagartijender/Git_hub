# Central Azure DevOps Pipeline Templates

`enterprise-microservice.yml` is the governed entry point consumed by every
microservice. It standardizes the stage order while allowing service teams to
provide language-specific build steps.

## Standard Lifecycle

1. Select the required runtime.
2. Scan the repository for secrets.
3. Prepare SonarQube analysis.
4. Run service-owned build and test steps.
5. enforce the SonarQube quality gate.
6. Package and publish the `drop` pipeline artifact.
7. Run Black Duck and Veracode policy scans.
8. Build and push an immutable image to ACR.
9. Commit the image tag to the GitOps repository.
10. Let ArgoCD reconcile the Helm release into AKS.

## Template Contract

Important required parameters:

| Parameter | Example |
|---|---|
| `serviceName` | `orders-api` |
| `language` | `python`, `node`, `java`, or `dotnet` |
| `runtimeVersion` | `3.12`, `22.x`, `21`, or `8.x` |
| `artifactPath` | `dist`, `target`, or `src` |
| `dockerfile` | `Dockerfile` |
| `imageRepository` | `orders-api` |
| `sonarProjectKey` | `orders-api` |
| `veracodeApplicationProfile` | `Orders API` |
| `gitopsValuesFile` | `apps/orders-api/environments/dev/values.yaml` |
| `buildSteps` | A typed Azure Pipelines `stepList` |

Optional security and delivery features are controlled by the `enable`
object. They default to enabled.

## External Repository Consumption

Store these templates in a dedicated Azure Repos repository and pin consumers
to a release tag:

```yaml
resources:
  repositories:
    - repository: centralTemplates
      type: git
      name: PlatformEngineering/central-pipeline-templates
      ref: refs/tags/v1.0.0

extends:
  template: pipelines/templates/enterprise-microservice.yml@centralTemplates
```

Use required-template approval and branch policies on the central repository.
Release template changes through semantic Git tags so teams can upgrade in a
controlled way.
