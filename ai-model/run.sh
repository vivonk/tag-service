#!/bin/sh

# Start the ollama server in the background
ollama serve &
ollama_pid=$!
# Wait for the server to start
sleep 10

echo "Pulling llama3:8b model"
# Pull the model
ollama pull llama3:8b

# Read the content of Modelfile into a variable
modelfile_content=$(tr '\n' '\n' < Modelfile)
model_name='tag-posts'

# Function to escape special characters for JSON
# Escape the content to be JSON compatible
escaped_modelfile_content=$(echo "$modelfile_content" | jq -Rsa .)

# Construct the JSON data manually
json_data=$(cat <<EOF
{
  "name": "$model_name",
  "modelfile": $escaped_modelfile_content,
  "stream": false
}
EOF
)


echo "Creating custom model ""$model_name"
# Make the curl request with the constructed JSON data
curl -POST http://localhost:11434/api/create -d "$json_data" -H "Content-Type: application/json"

# load the tag-posts model in-memory
json_lm_data=$(cat <<EOF
{
  "model": "$model_name",
  "stream": false
}
EOF
)
echo " Loading custom model $model_name in memory"
curl http://localhost:11434/api/generate -d "$json_lm_data" -H "Content-Type: application/json"
kill $ollama_pid
ollama serve