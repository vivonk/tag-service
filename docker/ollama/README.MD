1. create run.sh to download llama3 and then run it
2. create modelfile and create model by running the following command in run.sh
```curl
curl http://localhost:11434/api/create -d '{
  "name": "mario",
  "modelfile": "FROM llama3\nSYSTEM You are mario from Super Mario Bros."
}'
```
3. load model in memory by running the following command
```curl
curl http://localhost:11434/api/generate -d '{
  "model": "llama3"
}'
```