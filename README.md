# Overview

The AWI Install repository was created to simplify the process of installing AWI project.
AWI can be easily installed on any k8s cluster - either local one created with minikube,
kind or k3d or the ones such as EKS or GKE.

In the future, there will be also available a docker compose file for installing AWI
without the need for k8s at all.

## Prerequisites

In order to install AWI, the following things needs to be installed:

* Python3
* Python3 dependencies - the script requires installed dependencies from
    `requirements.txt`
* AWS CLI - for authenticating cluster with private registry, where our
    images are stored - it needs to be configured with access key
* kubectl - for interacting with our cluster, where AWI will be installed
* k8s cluster - it can be either local cluster installed with minikube or any
    other tool or external cluster from AWS/GCP etc. which you will have access
    with your kubectl
* go compiler - for initializing kubernetes operator (if needed)
* access to `app-net-interface` repositories

You need to install python3 dependencies for your project. You can do it by running

```sh
pip3 install -r requirements.txt
```

It is suggested to use `virtualenv` for that

## Deployment

To run the deployment simply run:

```sh
python3 deploy.py
```

To learn how to provide proper secrets to the project check the script helper

```sh
python3 deploy.py -h
```

## Contributing

Thank you for interest in contributing! Please refer to our
[contributing guide](CONTRIBUTING.md).

## License

awi-install is free and open-source software licensed under the *Apache 2.0*
License.

Refer to [our license file](./LICENSE).

awi-install is also made possible thanks to third party
[open source projects](./NOTICE)
