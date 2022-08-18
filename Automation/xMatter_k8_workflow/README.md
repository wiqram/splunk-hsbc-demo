# Kubernetes Steps

These steps allow you to interact with Kubernetes from xMatters.

---------

<kbd>
  <img src="https://github.com/xmatters/xMatters-Labs/raw/master/media/disclaimer.png">
</kbd>

---------

# Files

* [KubernetesSteps.zip](KubernetesSteps.zip) - Workflow zip file with the step and example flow
* [kubernetes.png](/kubernetes.png) - Kubernetes logo

# How it works
This step accesses the API through the xMatters Agent which will live in a pod inside your Kubernetes cluster.


# Installation

## Kubernetes Setup
The setup for Kubernetes involves creating a container image of the xMatters Agent, and then adding that to your Kubernetes cluster. 

Look [here](https://github.com/xmatters/xm-labs-xagent-on-kubernetes) for instructions on how to create a kubernetes deployment of the agent.


## xMatters Setup
1. Download the [KubernetesSteps.zip](KubernetesSteps.zip) file onto your local computer
2. Navigate to the Workflows tab of your xMatters instance
3. Click Import, and select the zip file you just downloaded
4. For any steps being used, run them on the xAgent in xMatters


## Usage
There are 3 steps included in this integration that can be used to interact with Kubernetes.

1. **Kubernetes - Get Pods** - This step gets information on the current pods.
2. **Kubernetes - Rollback Deployment** - This step runs `kubectl rollout undo` on a given deployment
3. **Kubernetes - Run Command** - This step takes a **parameters** input, which are the parameters it runs `kubectl` with on the agent.

### **Kubernetes - Get Pods**
---
### Outputs

| Name | Description |
| ---- | ----------  |
| result | raw output from kubectl get pods |
| result_pretty | html table version of result |
| exit_code | the exit code that occured. If this is other than 0 it may have failed. |

### **Kubernetes - Rollback Deployment**
---
### Inputs
| Name  | Required? | Min | Max | Help Text | Default Value | Multiline |
| ----- | ----------| --- | --- | --------- | ------------- | --------- |
| Deployment | Yes | 0 | 2000 | Name of the deployment to roll back | | No |

### Outputs

| Name | Description |
| ---- | ----------  |
| result | raw output from kubectl rollout undo |
| exit_code | the exit code that occured. If this is other than 0 it may have failed. |

### **Kubernetes - Run Command**
---
### Inputs
| Name  | Required? | Min | Max | Help Text | Default Value | Multiline |
| ----- | ----------| --- | --- | --------- | ------------- | --------- |
| Parameters | Yes | 0 | 2000 | This value is put after `kubectl` and run on the agent. | | No |

### Outputs

| Name | Description |
| ---- | ----------  |
| result | raw output from kubectl rollout undo |
| exit_code | the exit code that occured. If this is other than 0 it may have failed. |

## Example Flow
These are the three steps included in the flow.

<kbd>
<img src="media/ExampleFlow.png"\>
</kbd>
