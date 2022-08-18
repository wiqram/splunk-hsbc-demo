#FROM centos:latest
FROM centos:centos7

COPY xmatters.com.repo /etc/yum.repos.d/xmatters.com.repo

RUN yum -y install xmatters-xa && \
    touch /etc/xmatters/xa/auth.conf && \
    ln -sf /dev/stdout /var/log/xmatters/xmatters-xa/agent-communication-xmatters.log

COPY docker_entrypoint.sh /docker_entrypoint.sh

ENV FRIENDLY_NAME="xagent"
ENV WEBSOCKET_HOST="nttdemo.xmatters.com"
ENV WEBSOCKET_SECRET="Dt0rPFXSVJ78u6Kfioxo4CrN6NhQzuKc91KjDJYlvucgqK0f"
ENV OWNER_API_KEY="55c5841f-d291-406c-b182-3eeeef8f3dcd"

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin

ENTRYPOINT ["/docker_entrypoint.sh"]
CMD ["start"]
