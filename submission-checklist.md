1. Continuous model updates and deployment
   - any change in `ai-model/Modelfile` will trigger the CI/CD pipeline and deploy the model to the production environment
2. Automated updates
   - any new push on docker hub will be detected by the watcher container and the re-deployment will be trigger inside the k8s cluster
3. Scalability and Availability
   - Kubernetes cluster deployment is being used to make services auto scalable and highly available
   - Horizontal Pod Autoscaler (HPA) is used to scale the number of pods in a deployment based on observed resource utilization
   - Cloud platform services like SQS and DynamoDB are used to make the services infinite scalable and highly available
   - Load balancer is used to distribute the incoming traffic to the services