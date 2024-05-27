1. Continuous model updates and deployment
   - any change in `ai-model/Modelfile` will trigger the CI/CD pipeline and deploy the model to the production environment
2. Automated updates
   - any new push on docker hub will be detected by a watcher container and the re-deployment will be trigger for a service using the updated image
3. Scalability and Availability
   - Kubernetes cluster deployment is being used to make services auto scalable and highly available
   - Horizontal Pod Autoscaler (HPA) is used to scale the number of pods in a deployment based on observed resource utilization
   - Cloud platform services like SQS and DynamoDB are used to make the services infinite scalable and highly available
   - Load balancer is used to distribute the incoming traffic to the services, making things scalable and available
4. Deployment best practices
   - Security: 
     - All the deployments are done using the least privilege principle
     - Credentials are never exposed in the code and made available only through environment variables
     - All the internal services are deployed in a private subnet and are not directly accessible from the internet
   - Monitoring:
     - Cloudwatch is used to store the logs and metrics of the services
   - Process:
     - CI/CD pipeline is used to automate the deployment process
     - Manual steps are minimized and are only required at 1-2 places
     - All the deployments are done using the infrastructure as a code (IaaS)
     - 