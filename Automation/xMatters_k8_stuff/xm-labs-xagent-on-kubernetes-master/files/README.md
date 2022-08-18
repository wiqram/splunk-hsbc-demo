# Usage

## Build

    docker build -t xa:latest .

## Run

### Docker
----------
    docker run --name xa-whatever -d \
    -e WEBSOCKET_HOST=yourInstance.xmatters.com \
    -e WEBSOCKET_SECRET=xxx \
    -e OWNER_API_KEY=yyy \
    -e FRIENDLY_NAME=zzz \
    xa:latest

* `xa-whatever` is the name you want to give to your docker container
(easier to identify than default random ID)
* ...self-explanatory params
(these values are found in
Workflows > WORKFLOW TOOLS > Agents > Available
after you select centos7 in the dropdown)
* `FRIENDLY_NAME` is a string of your choosing that will be appended to `/default-`
in your XA's name in xMatters' UI.

This will create an xAgent in xMatters called:
> yourInstance-xmatters-com/default-zzz

#### Starting and Stopping

##### Stop the xAgent

    docker stop xa-whatever

##### Start the xAgent

    docker start xa-whatever

### Kubernetes
--------------

1. Update `kube/xagent.deploy.yaml` with the configuration for your environment
2. Update `kube/xagent.secrets.yaml` with the secrets for your environment
3. Deploy!

```
kubectl create -f kube/xagent.secrets.yaml
kubectl create -f kube/xagent.deploy.yaml
```
