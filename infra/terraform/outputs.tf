output "resource_group_name" {
  description = "Resource group created for the platform."
  value       = azurerm_resource_group.platform.name
}

output "acr_login_server" {
  description = "ACR login server used by application pipelines."
  value       = azurerm_container_registry.acr.login_server
}

output "aks_name" {
  description = "AKS cluster name."
  value       = azurerm_kubernetes_cluster.aks.name
}

output "aks_resource_group_name" {
  description = "AKS cluster resource group."
  value       = azurerm_kubernetes_cluster.aks.resource_group_name
}

output "log_analytics_workspace_id" {
  description = "Log Analytics workspace ID connected to AKS."
  value       = azurerm_log_analytics_workspace.aks.id
}

