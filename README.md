# Tag service
Tag service is designed to provide a way to tag posts in the forum.

# Architecture
https://miro.com/app/board/uXjVKKtdQdE=/?share_link_id=71865115152

This service is deployed in a Kubernetes cluster. The service is exposed to the internet using an AWS ELB.

### Components
1. AWS ELB - Load balancer - to distribute incoming traffic across multiple targets
2. Nginx Ingress Controller - to manage external access to services in a Kubernetes cluster
3. Tag service - to provide a way to tag posts in the forum
4. DynamoDB - to store posts with tags
5. Kafka - to process tag requests asynchronously
6. Tag request processor - to process tag requests asynchronously
7. AI Model service - to provide a way to generate tags for posts
8. Redis - to store frequently asked posts
9. Callback service - to provide a way to callback client about the status of the tag request
10. Log service - to store logs of the service

### Communication
1. The client sends a tag request to the Tag service through the AWS ELB.
2. The Tag service sends the tag request to the Kafka topic.
3. The Tag request processor processes the tag request and sends it to the AI Model service.
4. The AI Model service generates tags for the post and sends them back to the Tag request processor.
5. The Tag request processor stores the tags in DynamoDB.
6. The Tag request processor adds a completion event to Kafka with the status of the tag request.
7. The Callback service receives the completion event as consumer of Kafka topic and sends a callback to the client.

### Deployment
The Tag service is deployable as a Kubernetes cluster.
### CI/CD tooling
```shell
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```

### Local supported deployment through kubectl
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

### Local Deployment
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

### Docker Images
- ai-model-service
- tag-service
- tag-request-processor

Tag commands
```shell
docker tag ai-model-service:latest appsmithvivonk/ai-model-service:latest
docker tag tag-service:latest appsmithvivonk/tag-service:latest
docker tag tag-request-processor:latest appsmithvivonk/tag-request-processor:latest
```
Push commands
```shell
docker push appsmithvivonk/ai-model-service:latest
docker push appsmithvivonk/tag-service:latest
docker push appsmithvivonk/tag-request-processor:latest
```

### Security and Compliance
TODO

### Decision Log
Why Kubernetes?
- Kubernetes is a popular open-source container orchestration platform that can automate the deployment, scaling, and management of containerized applications.
- Kubernetes provides high availability and scalability. It can handle large volumes of traffic and can be easily scaled up or down.
- Kubernetes provides fault tolerance and self-healing. It can automatically restart failed containers and reschedule them on healthy nodes.
- Kubernetes provides declarative configuration and automation.
- Kubernetes provides monitoring and logging capabilities. It can collect metrics and logs from containers and nodes for debugging and analysis.
- Kubernetes provides security features such as network policies, RBAC, and secrets management. 

Why Kafka?
- Kafka is a distributed event streaming platform that can handle high throughput and low latency. It is a good choice for processing tag requests asynchronously.
- Kafka provides fault tolerance and scalability. It can handle large volumes of data and can be easily scaled up or down.
- Kafka provides durability and reliability. It can store messages for a configurable period of time and can replay messages in case of failure.
- Kafka provides a way to decouple the producer and consumer. It allows the producer to send messages without waiting for the consumer to process them.

Why DynamoDB?
- DynamoDB is a fully managed NoSQL database service provided by AWS. It is a good choice for storing posts with tags.
- DynamoDB provides high availability and durability. It can handle large volumes of data and can be easily scaled up or down.
- DynamoDB provides low latency and high throughput. It can handle read and write requests with millisecond latency.
- DynamoDB provides automatic scaling and backup. It can automatically scale up or down based on the workload and can take backups for disaster recovery.

Why Redis?
- Redis is an in-memory data store that can be used as a cache. It is a good choice for storing frequently asked posts.
- Redis provides high performance and low latency. It can handle read and write requests with sub-millisecond latency.

Why Nginx Ingress Controller?
- Nginx Ingress Controller is a popular open-source tool for managing external access to services in a Kubernetes cluster.
- Nginx Ingress Controller provides load balancing, SSL termination, and routing based on hostnames and paths.
- Nginx Ingress Controller provides high availability and scalability. It can handle large volumes of traffic and can be easily scaled up or down.
- Nginx Ingress Controller provides security features such as rate limiting, IP whitelisting, and SSL encryption.
- Nginx Ingress Controller provides monitoring and logging capabilities. It can log access and error logs for debugging and analysis.
- Nginx Ingress Controller provides integration with other tools such as Prometheus, Grafana, and ELK stack for monitoring and logging.

Why AWS ELB?
- AWS ELB is a managed load balancer service provided by AWS. It is a good choice for distributing incoming traffic across multiple targets.
- AWS ELB provides high availability and scalability. It can handle large volumes of traffic and can be easily scaled up or down.
- AWS ELB provides security features such as SSL termination, IP whitelisting, and DDoS protection.
- AWS ELB provides monitoring and logging capabilities. It can log access and error logs for debugging and analysis.
- AWS ELB provides integration with other tools such as Prometheus, Grafana, and ELK stack for monitoring and logging.
- AWS ELB provides integration with other AWS services such as CloudWatch, CloudTrail, and VPC for security and compliance.