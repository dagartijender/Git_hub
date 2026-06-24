variable "environment" {
  description = "Deployment environment name."
  type        = string
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "eastus"
}

variable "resource_group_name" {
  description = "Resource group name."
  type        = string
}

variable "acr_name" {
  description = "Globally unique Azure Container Registry name."
  type        = string
}

variable "aks_name" {
  description = "AKS cluster name."
  type        = string
}

variable "kubernetes_version" {
  description = "AKS Kubernetes version. Leave null to use Azure default."
  type        = string
  default     = null
}

variable "node_count" {
  description = "Initial node count for the default node pool."
  type        = number
  default     = 2
}

variable "node_vm_size" {
  description = "VM size for the default AKS node pool."
  type        = string
  default     = "Standard_DS2_v2"
}

variable "admin_group_object_ids" {
  description = "Azure AD group object IDs with AKS admin access."
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Common resource tags."
  type        = map(string)
  default     = {}
}

