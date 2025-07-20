# Required Operators
This project requires the following Kubernetes operators to be installed before deployment. 

## CloudNativePG
- Purpose: PostgreSQL dabatase management
- Version: 1.24.0
- Installation: 
```bash
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.24/releases/cnpg-1.24.0.yaml

# and to check
kubectl get pods -n cnpg-system
```
>Note: This will be improved with addition of helm charts next. 