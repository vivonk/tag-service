### Prerequisites
- Docker
- Python 3.x
- AWS Account
- AWS CLI configured with appropriate permissions
- PyCharm (optional)
 - .env file with necessary environment variables

### Create AWS SQS Queue
Create an SQS queue in your AWS account, and update the [.env file](local.env) with the necessary details.

# Setup for running in Local:

### Build and Run AI Model Service in Docker

Build and run the AI Model Service in Docker. The AI Model Service is a REST API that provides a stable endpoint to access the AI model.

```shell
docker buildx build --platform=linux/amd64 -t ai-model-service -f ai-model/Dockerfile ai-model/
docker run -d -p 11434:11434 --env-file .env ai-model-service
```

### Install Python Dependencies

````shell
pip install -r requirements.txt
````

### Run Tag Service and Tag Request Processor Locally

#### Running in PyCharm
- Open the project in PyCharm.
- Configure environment variables: Go to Run > Edit Configurations, select your run configuration, and set the environment variables from your .env file.
- Run the scripts:
- For the Tag Service, configure and run server.py.
- For the Tag Request Processor, configure and run tag_request_processor.py .

#### Running from Command Line

Alternatively, you can run the services from the command line:

- Load environment variables from the [.env](local.env) file:
```shell
export $(cat .env | xargs)
```
- Run the Tag Service:
```shell
python server.py
```
- Run the Tag Request Processor:
```shell
python tag_request_processor.py
```

### Local Deployment using Docker
- Setup Docker on your local
- add required details on .env file - copy env.example to .env and update the values
- create SQS queue in AWS and update the queue name in .env file
- Build & Run following docker images (from root director)
    - ai-model-service
      ```shell
      docker buildx build --platform=linux/amd64 -t ai-model-service -f ai-model/Dockerfile ai-model/
      docker run -d -p 11434:11434 ai-model-service
      ```
    - tag-service
      ```shell
        docker buildx build --platform=linux/amd64 -t tag-service -f DockerfileServer .
        docker run -d -p 11434:11434 --env-file .env tag-service
        ```
    - tag-request-processor
      ```shell
        docker buildx build --platform=linux/amd64 -t tag-request-processor -f DockerfileTRP .
        docker run -d --env-file .env tag-request-processor
        ```




# Setup to run in Kubernetes:

#### Deployment
The Tag service is deployable as a Kubernetes cluster.

#### CI/CD tooling
```shell
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```

#### Local supported deployment through kubectl
Here's the order in which you should apply these files to your Kubernetes cluster:

1. Namespace
2. Deployment
3. Service
4. Horizontal Pod Autoscaler (HPA)
5. Ingress

The reason for this order is that the namespace should exist before you can create resources within it. The deployment should exist before you create a service that selects it. The HPA needs the deployment to exist so it can scale it. The Ingress, if you have one, should be created last as it needs the service to exist to route traffic to it.

Here are the commands to apply these files:

1. Create the namespace and config maps:
  ```shell
  kubectl apply -f k8s/docket-namespace.yaml
  ```
Create env config map in k8s/config directory and apply the config map
  ```shell
      envsubst < configmap-template.yaml > configmap.yaml
      kubectl apply -f configmap.yaml
  ```
This command creates the namespace where your services, deployments, and other resources will reside.
2. Apply the deployments:
  ```shell
  kubectl apply -f k8s/deployment/tag-service.yaml
  kubectl apply -f k8s/deployment/tag-request-processor.yaml
  kubectl apply -f k8s/deployment/ai-model-service.yaml
  ```

These commands create the deployments for your services. Each deployment manages a set of identical pods, ensuring that they have the correct config and keeping the desired number of them operational.

3. Apply the services:

  ```shell
  kubectl apply -f k8s/service/tag-service.yaml
  kubectl apply -f k8s/service/ai-model-service.yaml
  ```

These commands create the services that provide a stable endpoint to access the pods managed by a deployment.

4. Apply the HPAs:
  ```shell
  kubectl apply -f k8s/hpa/tag-service.yaml
  kubectl apply -f k8s/hpa/tag-request-processor.yaml
  kubectl apply -f k8s/hpa/ai-model-service.yaml
  ```
These commands create the Horizontal Pod Autoscalers for your deployments. The HPA automatically scales the number of pods in a deployment based on observed CPU utilization.

5. Apply the Ingress:

  ```shell
  kubectl apply -f k8s/ingress-nginx-service.yaml
  kubectl apply -f k8s/tag-service-ingress.yaml
  ```
These commands create the Ingress resources. The Ingress exposes HTTP and HTTPS routes from outside the cluster to services within the cluster.

#### Docker Images
- ai-model-service
- tag-service
- tag-request-processor

#### Tag commands
```shell
docker tag ai-model-service:latest appsmithvivonk/ai-model-service:latest
docker tag tag-service:latest appsmithvivonk/tag-service:latest
docker tag tag-request-processor:latest appsmithvivonk/tag-request-processor:latest
```
#### Push commands
```shell
docker push appsmithvivonk/ai-model-service:latest
docker push appsmithvivonk/tag-service:latest
docker push appsmithvivonk/tag-request-processor:latest
```
