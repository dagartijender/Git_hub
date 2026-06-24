environment         = "staging"
location            = "eastus"
resource_group_name = "rg-gitops-platform-staging"
acr_name            = "acrplatformstg001"
aks_name            = "aks-gitops-staging"
node_count          = 2
node_vm_size        = "Standard_DS2_v2"

tags = {
  cost_center = "platform"
  workload    = "microservices"
}

