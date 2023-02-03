FROM python:latest
WORKDIR /usr/app/src
RUN pip install --no-cache-dir --upgrade pip \
  && pip install requests \
  && pip install python-dateutil
RUN set -x && \
    apt-get update && apt-get install -y\
    openssl
  #json
COPY venafi.py ./
COPY cert.csr ./
COPY key.pem ./
COPY cert.pem ./
#RUN openssl pkcs12 -help
CMD [ "python", "-u","./venafi.py"]
