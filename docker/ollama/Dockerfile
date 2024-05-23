FROM ollama/ollama
COPY run.sh /opt/models/
COPY Modelfile /opt/models/
WORKDIR /opt/models
RUN chmod +x run.sh
RUN apt install jq curl -y
CMD ["/bin/ollama", "serve"]
ENTRYPOINT ["./run.sh"]
