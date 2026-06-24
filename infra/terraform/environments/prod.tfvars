environment         = "prod"
location            = "eastus"
resource_group_name = "rg-gitops-platform-prod"
acr_name            = "acrplatformprod001"
aks_name            = "aks-gitops-prod"
node_count          = 3
node_vm_size        = "Standard_DS3_v2"

tags = {
  cost_center = "platform"
  workload    = "microservices"
}

