Want to update the model?
- Update the model file `Modelfile`
How does model run?
- The model runs as docker image
How to run the model?
- ```shell
    docker buildx build --platform=linux/amd64 -t ai-model-service -f ai-model/Dockerfile ai-model/
    docker run -d -p 11434:11434 ai-model-service
  ```