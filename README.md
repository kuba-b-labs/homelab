# Homelab with ArgoCD

<div align="center">

<img src="https://img.shields.io/badge/Kubernetes-326CE5.svg?style=default&logo=kubernetes&logoColor=white" alt="Kubernetes">
<img src="https://img.shields.io/badge/ArgoCD-1F1F1F.svg?style=default&logo=argo&logoColor=white" alt="ArgoCD">
<img src="https://img.shields.io/badge/Kustomize-7B42BC.svg?style=default&logo=kubernetes&logoColor=white" alt="Kustomize">
<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=default&logo=YAML&logoColor=white" alt="YAML">
<img src="https://img.shields.io/badge/JSON-000000.svg?style=default&logo=JSON&logoColor=white" alt="JSON">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=default&logo=docker&logoColor=white" alt="Docker">

</div>

---

## Overview

A GitOps-based Kubernetes homelab infrastructure managed by ArgoCD on 2 nodes. This repository contains the declarative configuration for applications, monitoring, database infrastructure, and external secret management across multiple environments.
Additionally backups for databases are stored in Azure Storage Accounts and secrets are pulled from Azure Key Vault.

## Architecture

### Core Components

- **ArgoCD**: GitOps continuous deployment tool for Kubernetes applications
- **Kustomize**: Template-free customization for Kubernetes YAML manifests
- **Operators**: Kubernetes operators for managing complex application lifecycle
- **External Secrets**: Secure secrets management with Azure integration
- **CNPG**: CloudNativePG for PostgreSQL database management
- **Monitoring Stack**: Prometheus, Grafana, AlertManager, and Kube State Metrics

## Project Organization

### ArgoCD Configuration
Contains the core ArgoCD setup and bootstrapping logic:
- Application of Applications pattern for hierarchical management
- ArgoCD core components and configuration
- Helm integration support
- Application set definitions for both applications and operators

### Application Deployments
Deployable applications with multi-environment support:
- Base configurations with environment-specific overrides

### Infrastructure Components
Core system infrastructure:
- **CloudNativePG**: PostgreSQL database management with automated backups and monitoring
- **External Secrets**: Azure integration for secure secrets synchronization
- **Kubernetes Operators**: Lifecycle management for complex infrastructure components
- **Argocd kustomize enabled for using helm charts**

### Monitoring & Observability Stack
Complete observability solution:
- **Prometheus**: Metrics collection and alerting rule management
- **Grafana**: Visualization with pre-configured dashboards
- **AlertManager**: Alert routing and aggregation (Discord notifications)
- **Kube State Metrics**: Kubernetes cluster and object metrics

##  Getting Started

### Prerequisites
- Kubernetes cluster (v1.20+)
- ArgoCD installed on the cluster
- kubectl configured to access your cluster
- Git repository access to this repository

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kuba-b-labs/homelab.git
cd homelab
```

2. **Deploy ArgoCD with app-of-apps pattern**
```bash
kubectl create namespace argocd
kubectl apply -f argocd/argocd-bundle.yaml
kubectl apply -f argocd/app-of-apps.yaml
```

3. **Configure environment overrides**
   - Modify files in `envs/dev/` directories for your environment
   - Update `kustomization.yaml` files as needed

4. **Sync applications**
```bash
# Monitor ArgoCD UI or use kubectl
kubectl get applications -n argocd
```

## Key Features

### GitOps Workflow
- Declarative configuration stored in Git
- Automated synchronization via ArgoCD
- Self-healing and automatic pruning enabled
- Application of Applications (AppOfApps) pattern for hierarchical management

### Multi-Environment Support
- Base configurations in `/base` directories
- Environment-specific overrides in `/envs/<environment>` directories
- Easy environment promotion and replication

### Database Management
- CloudNativePG for PostgreSQL operators
- Automated backups with scheduled policies
- Integrated monitoring with postgres-exporter
- Secrets stored securely via External Secrets Operator

### Secrets Management
- Azure integration via External Secrets Operator
- Service principal authentication
- Automatic secret synchronization from Azure Key Vault

### Comprehensive Monitoring
- Prometheus for metrics collection
- Grafana for visualization
- AlertManager for alert routing
- Kube State Metrics for cluster insights
- Pre-configured dashboards and rules

## Monitoring Stack Setup

### Grafana Dashboards
Access Grafana to view pre-configured dashboards:
- Basic dashboard
- Default cluster dashboard
- Custom application metrics

### Prometheus Targets
Prometheus discovers and scrapes metrics from:
- Kubelet metrics
- Node exporter
- Application pods
- Custom endpoints (see `targets/targets.json`)

### Alerts
AlertManager routes and manages alerts defined in Prometheus rules (`monitoring/prometheus/base/rules/rules.yaml`)

## Secrets Management

External Secrets Operator integrates with Azure:
1. Service principal authentication - need to be added manually in argocd namespace
2. Cluster secret store configuration (`cluster-secret-store.yaml`)
3. Automatic secret syncing to Kubernetes secrets

## Customization

### Adding a New Application
1. Create directory under `/apps/<app-name>/`
2. Set up `base/kustomization.yaml` with resources
3. Create `envs/dev/kustomization.yaml` for overrides
4. Add application to `app-sets/dev-appset-apps.yaml`

### Adding Infrastructure Components
1. Create directory under `/infrastructure/<component>/`
2. Follow the same base/envs structure
3. Reference in ArgoCD applications

### Environment-Specific Changes
Edit the `kustomization.yaml` files in `envs/<environment>/` directories:
```yaml
# Example: apps/linkding/envs/dev/kustomization.yaml
bases:
  - ../../base
patchesStrategicMerge:
  - linkding_deployment.yaml
```

## Configuration Files

### Kustomization Files
- Define base resources
- Specify patches and overlays
- Configure namespaces and labels

### Deployment Manifests
- Service configurations
- Deployment specifications
- PersistentVolumeClaim definitions
- ConfigMaps and Secrets

### ArgoCD Sync Policy
- `automated.prune: true` - Remove resources deleted from Git
- `automated.selfHeal: true` - Revert manual cluster changes
- Custom sync options for server-side apply and replacement

## Workflow

1. **Commit changes** to this Git repository
2. **ArgoCD detects** the changes automatically
3. **Applications sync** according to the sync policy
4. **Monitor** progress via ArgoCD UI or CLI

```bash
# Check application sync status
argocd app list

# Sync an application manually
argocd app sync <app-name>
```

## Operators

The infrastructure includes several Kubernetes operators:
- **CloudNativePG**: PostgreSQL database management
- **External Secrets**: Secrets synchronization from external vaults

## Monitoring and Logging

Access monitoring components:
- **Prometheus**: Cluster metrics and alerting
- **Grafana**: Dashboards and visualization
- **AlertManager**: Alert aggregation and routing, alerts are send to discord channel
- **Kube State Metrics**: Kubernetes object metrics

