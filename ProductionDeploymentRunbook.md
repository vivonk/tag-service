This guide will walk you through how to deploy tag service into production.

We have setup the CI/CD pipeline in such a way that whenever a new commit is detected in the master branch, the pipeline will be triggered and the tag service will be deployed to the production environment.

Most of the process is streamlined and is automated. However, there are some manual steps that need to be followed to deploy the tag service to production.
1. Configuring variables and secrets in GitHub repository
   1. secrets - 
        ```shell
        AWS_ACCESS_KEY_ID
        AWS_ACCOUNT_ID
        AWS_DEFAULT_REGION
        AWS_SECRET_ACCESS_KEY
        DOCKER_HUB_ACCESS_TOKEN
        DOCKER_HUB_USERNAME
      ```
   2. variables - 
      ```shell
        AI_SERVICE_URL - url of the ai model service
        DLQ_NAME - dead letter queue name defined in terraform file sqs.tf
        EKS_CLUSTER_NAME - name of the eks cluster defined in terraform file main.tf
        MODEL_NAME - name of the ai model defined in the ai model service
        QUEUE_NAME - queue name defined in terraform file sqs.tf
        ```
2. Once the variables and secrets are configured, workflows can be triggered by pushing the changes to the master branch.
3. Workflows and their workings:
   1. build-push: This workflow builds the docker image and pushes it to the docker hub.
   2. terraform-deploy: This workflow applies the terraform scripts to create the required resources in AWS.
   3. k8s-deploy: This workflow applies the kubernetes manifests to deploy the tag service to the production environment.
4. If we are creating an environment for the first time, make dummy/real changes into the apps, terraform files and k8s manifest files to trigger the workflows.
    - In-case you want to create a new environment, make sure to update the terraform files with the new environment details and update the k8s manifest files accordingly
5. Once changes are merged into master, all the workflows will be triggered and the tag service will be deployed to the production environment.
6. Whenever we create a new environment for the first time, expectation is, it is deployed first time with some manual step executions and then onwards it will be automated. <br> In our case, we have two components we need to deploy manually that's ingress controller and keel because we don't want to make the changes to ingress controller frequently, and it is a one time setup.
7. Once we have deployed the complete infrastructure using terraform, and applied the k8s manifest files using workflows, we need to deploy the ingress controller to expose the tag service to the internet.
8. To deploy the ingress controller, follow the below steps
   - Make sure you have helm installed in your local machine and kubeconfig is pointing to the production cluster.
   - Add the ingress-nginx repository to helm:
      ```shell
      helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
      ```
   - Install the ingress-nginx chart:
      ```shell
      helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
      ``` Deploy the ingress controller:
   
9. Once the ingress controller is deployed, the tag service will be accessible to the internet.
10. To make our services automatically update whenever a new image is pushed to the docker hub, we need to install a watcher container running in the production environment.
    - Tool: keel
    - Installation steps:
      ```shell
      helm repo add keel https://charts.keel.sh 
      helm upgrade --install keel --namespace=kube-system keel/keel
      ```
11. Once the watcher container is installed, it will detect the changes in the docker hub and trigger the re-deployment of the tag service using the updated image.