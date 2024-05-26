# Document on how to setup GitHub workflows for CI/CD
This document will guide you on how to setup GitHub workflows for CI/CD. The CI/CD workflow will be triggered on every push to the main branch. 
The workflow will build the Docker image, push it to the Docker Container Registry, and deploy the image to the Kubernetes cluster.

## Prerequisites
### Infrastructure setup
We use Terraform to setup the infrastructure. You can find the Terraform scripts in the `terraform` directory.

How to setup the infrastructure:

