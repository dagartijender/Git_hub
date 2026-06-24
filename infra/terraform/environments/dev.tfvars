environment         = "dev"
location            = "eastus"
resource_group_name = "rg-gitops-platform-dev"
acr_name            = "acrplatformdev001"
aks_name            = "aks-gitops-dev"
node_count          = 2
node_vm_size        = "Standard_DS2_v2"

tags = {
  cost_center = "platform"
  workload    = "microservices"
}

