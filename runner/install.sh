#!/bin/bash
# Create a folder
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.316.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.316.1/actions-runner-linux-x64-2.316.1.tar.gz
tar xzf ./actions-runner-linux-x64-2.316.1.tar.gz
export RUNNER_ALLOW_RUNASROOT="1"
# Create the runner and start the configuration experience
./config.sh --url https://github.com/vivonk/tag-service --token AGDHB6RBM2JAX6DNMOQHLNDGKSQFI
./run.sh