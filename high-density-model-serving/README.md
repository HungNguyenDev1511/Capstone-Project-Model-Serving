# How-to Guide

## Prerequisites

### Install kustomize
[Kustomize](https://kubectl.docs.kubernetes.io/) is another tool to install applications on k8s beside Helm. Let's install it first.

```shell
curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash
sudo mv kustomize /usr/local/bin/
```

### Install modelmesh-serving

Pay attention that `minikf` uses Kubernetes version 1.16, which is not suitable for the latest release of the modelmesh-serving repository, which is `0.11.1`.

Clone the repository. I did this step already for you so you don't have to redo this. I just want to show you what I did.
```shell
RELEASE=release-0.8
git clone -b $RELEASE --depth 1 --single-branch https://github.com/kserve/modelmesh-serving.git
cd modelmesh-serving
```

Create a new namespace and install modelmesh-serving
```shell
kubectl create namespace modelmesh-serving
./scripts/install.sh --namespace modelmesh-serving --quickstart

```

After several minutes, you should see the following output
![modelmesh-serving](./images/modelmesh-serving-installation.png)

## Quickstart

Port-forward `minio` service so you can access it locally
```shell
kubectl port-forward svc/minio -p 9000:9000 -n modelmesh-serving
```

Assume that your `minio` pod is `minio-5f894ffd9-v27zp`, use the following commands to obtain `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` for signing in `minio` and uploading your objects.

```shell
kubectl get po minio-5f894ffd9-v27zp -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_ACCESS_KEY") | .value'

kubectl get po minio-5f894ffd9-v27zp -o json | jq -r '.spec.containers[0].env[] | select(.name == "MINIO_SECRET_KEY") | .value'
```

You can see that in my case, `MINIO_ACCESS_KEY` is `AKIAIOSFODNN7EXAMPLE`, and `MINIO_SECRET_KEY` is `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`.
![minio-credentials](./images/minio-credentials.png).


Run the following command to have a quickstart model
```shell
kubectl apply -f deployments/quickstart.yaml
```

To see whether our service is ready, run the following command
```shell
kubectl get isvc
```
, it should take several minutes for our service to be `READY`. If not, please check logs of the container `mm` in the pod corresponding to `mlserver` as follows

```shell
kubectl logs modelmesh-serving-mlserver-0.x-68d7dcb75d-5m5lg -c mm
```

To make a prediction, do the following steps:

1. Port-forward `modelmesh-serving` service
    ```shell
    kubectl port-forward --address 0.0.0.0 service/modelmesh-serving 8008 -n modelmesh-serving
    ```
2. Test your newly created modelmesh-serving service
    ```shell
    python utils/quickstart/client.py
    ```

    **Note:** Don't forget to replace your cookie ;)

## Custom Server
1. Build the corresponding image
    ```shell
    cd intrusion-detection-runtime
    bash build.sh
    ```

    **Note:** Please update your docker username properly in the file `build.sh` before doing the above steps.

2. Create a new serving runtime name `vae-0.x`
    ```shell
    cd intrusion-detection-runtime
    kubectl apply -f vae-servingruntime.yaml
    ```

    **Note:** Similar to the above step, replace your recently built image.
3. Create a new `isvc` residing in the runtime `vae-0.x`
    ```shell
    kubectl apply -f intrusion-detection.yaml
    ```
4. Enjoy your newly created service
    ```shell
    conda create -n mm python=3.9
    conda activate mm
    pip install -r requirements.txt
    python utils/anomaly/anomaly_client.py
    ```
