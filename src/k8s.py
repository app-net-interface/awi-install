import tempfile
import time

from kubernetes import client, utils
from kubernetes import config as k8s_config

from .template import render_from_yaml


class K8sClientException(Exception):
    def __init__(self, msg = None, exception = None):
        self._msg = msg
        self._e = exception
    
    def __str__(self):
        msg = "The k8s client failed to perform the operation."
        if self._msg is not None:
            msg += f" {self._msg}."
        if self._e is not None:
            msg += f" Got exception: {self._e}"
        return msg


class K8sClient():
    def __init__(self, kubeconfig = None):
        k8s_config.load_kube_config(kubeconfig)
        self._v1 = client.CoreV1Api()
        try:
            self._v1.list_namespace()
        except Exception as e:
            raise K8sClientException(
                msg=f"The k8s client doesn't have access to cluster. "
                "Did you specify correct kube config file?",
                exception=e
            )


    def create_namespace(self, namespace):
        try:
            self._v1.create_namespace(client.V1Namespace(
                metadata=client.V1ObjectMeta(name=namespace)
            ))
            
        except client.ApiException as e:
            raise K8sClientException(
                msg=f"Failed to create namespace '{namespace}'",
                exception=e
            )


    def apply_manifest(self, manifest, namespace=None):
        try:
            utils.create_from_yaml(k8s_client=client.ApiClient(), yaml_file=manifest, namespace=namespace)
        except client.ApiException as e:
            raise K8sClientException(
                msg=f"Failed to apply manifest '{manifest}'",
                exception=e
            )


    def apply_template_manifest(self, template_manifest, vars):
        documents = render_from_yaml(template_manifest, vars)
        for d in documents:
            with tempfile.NamedTemporaryFile() as f:
                f.write(d.encode('utf-8'))
                f.flush()
                self.apply_manifest(f.name)
