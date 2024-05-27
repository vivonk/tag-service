This document describes how the current CI/CD configuration works and how does the complete workflow looks like.

1. Docker: For builds
2. Terraform: For infrastructure
3. Kubernetes: For deployment

Combining individual CI/CD workflows for each of the above components, we have a complete CI/CD pipeline for the tag service.
Here are list of workflows and their working:
1. Build and Push workflow: (build-push.yaml) This workflow will trigger for any new change in master branch and specific paths.<br> It will build the docker image and push it to the docker hub.
2. Terraform Deploy workflow: (terraform-deploy.yaml) This workflow will trigger for any new change in master branch and specific path `terraform/`.<br> It will apply the terraform scripts to create the required resources in AWS.
3. Kubernetes Deploy workflow: (k8s-deploy.yaml) This workflow will trigger for any new change in master branch and specific path `k8s/`.<br> It will apply the kubernetes manifests to deploy the tag service to the production environment.

There is a hidden component of CD process which is not part of automated workflows: 
1. Whenever a new image is pushed to the docker hub, a watcher container running in the production environment will detect the change and trigger the re-deployment of the service using the updated image.
2. We are using [Keel](https://keel.sh) for this purpose. Keel is a tool that automates the deployment of container images to Kubernetes.

Scope of improvement with the current setup:
- Adding CI integration for testing