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
     - Manual steps are minimized and are only required at 1-2 places (one-time setups)
     - All the deployments are done using the infrastructure as a code (IaaS), configurations
5. Compliance: 
   - All the services are deployed in a secure and compliant way
   - Data is always encrypted in transit and at rest with SQS and DynamoDB

### Test out the service
 Live Hosting URL: http://ab375f2b3c43e44099cd13254ae94934-30142821.ap-south-1.elb.amazonaws.com 
1. Add a new post for tag
   - POST `/post/tag`
   - Request Body:
     ```json
     {
        "post_id": "13",
        "content": "I am facing a lot of problems with creating partitions in Kafka using shell command, is there any automated way in Java for recreating the partitions?"
     }
     ```
2. Get tags for a post
   - GET `/post/{post_id}`
   - Response:
     ```json
     {
        "post_id": "13",
        "tags": ["kafka", "java", "shell"]
     }
     ```

When model initially runs, it will take some time to load the model and start serving the requests. You can check the logs of the AI Model service to see the status of the model loading.
But once model is loaded, it will start serving the requests quickly.
First post tag request might take approx 2-3 minutes to generate the tags as model loads in memory, generate response and then tags will be available in the DB but subsequent requests will be faster and tags will be available in the DB within seconds.

### Testing CI/CD workflows
You can test out the workflows by making changes in the code and pushing them to the master branch. The workflows will be triggered automatically and the changes will be deployed to the production environment.
I am not actively running the GitHub self-hosted runner for this. If required, let me know, I will start the runner, and you can test the workflows.