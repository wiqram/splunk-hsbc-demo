# xAgent on Kubernetes

Instructions on how to run the xAgent in Kubernetes.

---------

<kbd>
  <img src="https://github.com/xmatters/xMatters-Labs/raw/master/media/disclaimer.png">
</kbd>

---------

# Files

* [/files](/files) - Files for creating and deploying the xAgent container.

# Installation

## Docker Setup

1. Run `docker build -t <CONTAINER_REGISTRY_LOCATION>:latest .` in [/files](/files) to create a docker image
2. Run `docker push <CONTAINER_REGISTRY_LOCATION>` to push the container up to the container registry

## Kubernetes Setup

1. Modify the [/files/kube/xagent.deploy.yaml](/files/kube/xagent.deploy.yaml) file
    1. On line 20, insert the image location. This is the container registry location.
    2. On line 23, change the xmatters url for your instance.
    3. On line 35, change the friendly name value. This is what your agent's name will be in xMatters.
2. Modify the [/files/kube/xagent.secrets.yaml](/files/kube/xagent.secrets.yaml) file
    1. Find your API Key and Secret in xMatters. These values can be found in the xMatters installation instructions `Workflows > Agents` in your xMatters instance.
    2. Base64 decode these values. A simple way to do this is to run:
        1. `echo -n "VALUE" | base64 -d` in bash on linux
        2. `echo -n "VALUE" | base64 -D` on macOS
    3. Put those values in the [/files/kube/xagent.secrets.yaml](/files/kube/xagent.secrets.yaml) file.
3. Modify the xmatters service account file
    1. The [/files/role.yaml](/files/role.yaml) file contains a sample list of permissions. Change these as needed for which permissions you need the xAgent to have.
4. run `kubectl apply -f files/role.yaml` to create the xmatters service account.
5. run `kubectl create -f files/kube/xagent.secrets.yaml` to put the secrets into Kubernetes.
6. run `kubectl create -f files/kube/xagent.deploy.yaml` to create the deployment.


