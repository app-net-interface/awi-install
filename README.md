# Overview

The AWI Install repository was created to simplify the process of installing AWI project.
AWI can be easily installed on any k8s cluster - either local one created with minikube,
kind or k3d or the ones such as EKS or GKE.

# Prerequisites

Installing App Net Interface requires:

* k8s cluster - it can be either local cluster installed with minikube or any
    other tool or external cluster from AWS/GCP etc. which you will have access
    with your kubectl

* credentials - depending on the details of controller in use, several secrets
    may be required. More about them [here](#creating-secrets)

* kubectl - for creating k8s secrets

* helm - for deploying App-Net-Interface on a cluster

# Running App Net Interface

Installing App Net Interface on your cluster involves a few steps

1. Creating necessary secrets in your k8s cluster
1. Setting up private registry if required
1. Deploying App-Net-Interface using Helm

## Creating Secrets

Before deploying App Net Interface, the administrator should create all
necessary secrets first. App Net Interface manifests are prepared to
expect certain secrets so if those are not provided, the k8s pods will
fail to initialize.

**Each secret value needs to be base64 encoded.**

For instance, a secret `catalyst-sdwan-credentials` which requires username and
password set to admin/password123 will look like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: catalyst-sdwan-credentials
type: Opaque
data:
  username: "YWRtaW4K"
  password: "cGFzc3dvcmQxMjMK"
```

Such secret can be later deployed running

```
kubectl apply -f YAML_FILE -n NAMESPACE
```

**Secrets needs to be stored in the same namespace where App Net Interface**
**will be deployed!**

Current App Net Interface defines following secrets.

* catalyst sdwan credentials
* cloud provider's credentials
* ui credentials
* kubernetes context

Currently, there are no mandatory credentials. Depending on the App Net
Interface configuration, some of them are required and some not.

### Python script

To not create all scripts manually, there is a python script
`generate_secrets.py` which can be used to automatically render and
deploy necessary secrets.

```
AWI_GCP_CREDENTIALS_FILE="PATH_TO_JSON_FILE" python3 generate_secrets.py
```

To view the list of available arguments run:

```
python3 generate_secrets.py --help
```

Currently, script names are not customizable, they are expected to be
named as described below.

### Catalyst SDWAN Credentials

Needed when App Net Interface uses Catalyst SDWAN as a connector

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: catalyst-sdwan-credentials
type: Opaque
data:
  username: "{CATALYST_SDWAN_USERNAME}"
  password: "{CATALYST_SDWAN_PASSWORD}"
```

### Provider specific credentials

If the App Net Interface connector is set to AWI, the administrator
needs to provide secrets required for using AWS/GCP providers.

The AWS secret currently expects base64 encoded `credentials` file
such as `$HOME/.aws/credentials`:

```ini
[default]
aws_access_key_id = KEY
aws_secret_access_key = VALUE
```

and such base64 encoded file should be placed inside a following secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: aws-credentials
type: Opaque
data:
  credentials: "{FILE_ENCODED}"
```

Similarly, GCP credentials also require base64 encoded file, which can be
found under `$HOME/.config/gcloud`. The example file content:

**Service Account is required.**

```json
{
  "client_email": "CLIENT_EMAIL",
  "client_id": "CLIENT_ID",
  "private_key": "PRIVATE_KEY",
  "private_key_id": "PRIVATE_KEY_ID",
  "token_uri": "TOKEN_URI",
  "type": "service_account"
}
```

And such base64 encoded file should be put in following secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gcp-credentials
type: Opaque
data:
  gcp-key.json: "{FILE_ENCODED}"
```

### Cluster Context

If the administrator wants App Net Interface to be able to interact with
k8s cluster (discovery process or creating connections to pods) the kubeconfig
file needs to be provided as a secret (base64 encoded):

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kube-config
type: Opaque
data:
  config: "{FILE_ENCODED}"
```

### UI Credentials

Currently, UI credentials are completely optional even if UI
is spawned. The UI expects:

* GOOGLE_MAPS_API_KEY
* IP2LOCATION_API_KEY

for geographic data purposes but these are not mandatory and not
required for the UI to work with App Net Interface

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: awi-ui-keys
type: Opaque
data:
  google_maps_api_key: "{GOOGLE_MAPS_API_KEY}"
  ip2_location_api_key: "{IP2LOCATION_API_KEY}"
```

## Setting up Private Registry

This step is required if App Net Interface will use a private
registry to pull images.

To use private registry it is important to override default
values to explicitely mention that private registry is in use
and what is the name of such registry.

Creating your own registry rather than using registries such
as gcr.io etc. may require additional steps.

### Example command for creating AWS Registry

```bash
kubectl create secret docker-registry ausm-private-registry \
    -n NAMESPACE \
    --docker-server=REGISTRY.dkr.ecr.us-west-2.amazonaws.com \
    --docker-username=AWS \
    --docker-password="$(aws ecr get-login-password --region us-west-2)"
```

### Example command for creating GHCR Registry

```bash
kubectl create secret docker-registry ausm-private-registry \
  -n NAMESPACE \
  --docker-server=ghcr.io \
  --docker-username=GITHUB_USERNAME \
  --docker-password=GHCR_PAT \
  --docker-email=your-email@example.com
```

## Deploying App Net Interface using Helm

After you've created necessary secrets and optional private registry
secret, you can install awi on your cluster using helm.

To install it from local repository, go to `awi-install/helm` directory
and type:

```
helm install awi . --namespace awi-system
```

# Building chart

## Chart overview

The AWI project consists of two charts:

1. main chart - the chart containing manifests for most of AWI components that include:

    * AWI GRPC Catalyst Sdwan - the main operational controller
    * AWI Infra Guard - component responsible for setting connections using AWI connector
    * AWI UI - the front-end for the application
    * Envoy Proxy - a proxy image for forwarding requests to proper targets and handling
        WebGRPC protocol used by the UI

1. operator chart - the second chart responsible for kube-awi component that allows
    spawning k8s operator and necessary CRDs

## Building

Creating a new `main chart` simply requires updating templates, `Chart.yaml` and `values.yaml`
according to your needs, however `operator chart` involves a few different steps.

### Operator Chart

The `operator chart` is built automatically from the `kube-awi` repository using `helmify`
tool. If the kube-awi repository did not change, there should be no need in rebuilding
operator chart.

If the operator chart needs to be refreshed:

1. Initialize submodules to download kube-awi repository

    ```
    make init-submodules
    ```

1. Ensure kube-awi is recent

    ```
    cd kube-awi
    git checkout main
    git pull origin main
    cd ..
    ```

1. Make sure kube-awi is kustomized accodringly to the project needs.  If not, enter
    kube-awi directory, kustomize it and optionally commit changes.

    The project's production kustomize configuration should be commited so this step
    is mostly for building custom charts.

1. Generate chart

    ```
    make build-operator-graph
    ```

1. Update `main chart` Chart.yaml with a new dependency version of your operator chart

# Contributing

Thank you for interest in contributing! Please refer to our
[contributing guide](CONTRIBUTING.md).

# License

awi-install is free and open-source software licensed under the *Apache 2.0*
License.

Refer to [our license file](./LICENSE).

awi-install is also made possible thanks to third party
[open source projects](./NOTICE)
