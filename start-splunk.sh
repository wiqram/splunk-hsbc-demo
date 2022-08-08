docker pull splunk/splunk
docker run -d -p 8000:8000 -e "SPLUNK_START_ARGS=--accept-license" -e "SPLUNK_PASSWORD=Password@1" --name splunk splunk/splunk:latest