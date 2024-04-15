# How-to Guide

## Build the project

1. Multi-worker training
    ```shell
    cd multi-worker-training
    bash build.sh
    kubectl apply -f mwt.yaml
    ```

2. Parameter-server training
    ```shell
    cd parameter-server-training
    bash build.sh
    kubectl apply -f pst.yaml
    ```

## Investigate the models

Update `persistentVolumeClaim` in the file `tests/nginx.yaml` with:
- `pst-volume` if you want to see the `pst` model
- `mwt-volume` if you want to see the `mwt` model

    ```shell
    kubectl apply -f tests/nginx.yaml
    kubectl exec -ti nginx bash
    ```

# References

For more information, please take a look at examples [here](https://github.com/kubeflow/training-operator/tree/master/examples) and [here](https://github.com/kubeflow/examples/tree/master/github_issue_summarization).

Some other useful examples:
- https://henning.kropponline.de/2017/03/19/distributing-tensorflow/
- https://www.cs.cornell.edu/courses/cs4787/2019sp/notes/lecture22.pdf
- https://web.eecs.umich.edu/~mosharaf/Readings/Parameter-Server.pdf
- https://s3.us.cloud-object-storage.appdomain.cloud/developer/default/series/os-kubeflow-2020/static/kubeflow06.pdf
- https://xzhu0027.gitbook.io/blog/ml-system/sys-ml-index/parameter-servers
- http://www.juyang.co/distributed-model-training-ii-parameter-server-and-allreduce/