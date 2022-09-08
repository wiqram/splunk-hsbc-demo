FROM python:latest
WORKDIR /usr/app/src
RUN pip install --no-cache-dir --upgrade pip \
  && pip install requests \
  && pip install python-dateutil
  #json
COPY venafi.py ./
COPY domain.csr ./
CMD [ "python", "-u","./venafi.py"]