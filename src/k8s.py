import tempfile
import time

from kubernetes import client, utils
from kubernetes import config as k8s_config

from .cmd import run_cmd
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


    def purge_namespace(self, namespace):
        """
        Removes everything created within the given namespace.

        The namespace is deleted afterwards if there are no
        errors in the meantime.

        The purge uses kubectl binary underneath as a workaround
        for a lack of generic deletion of subresources.
        """
        ok, result = run_cmd(f"kubectl delete all --all -n {namespace}")
        if not ok:
            raise K8sClientException(
                msg=f"Could not clean up the namespace: {result}."
                "The purge method uses kubectl binary installed on the host "
                "instead of k8s API as the rest of the script due to the lack "
                "of generic resource deletion. It is a workaround. "
                "Check if your kubectl can access the cluster - otherwise "
                " you may want to clean namespace yourself."
            )
        self.delete_namespace(namespace)


    def namespace_exists(self, namespace):
        try:
            self._v1.read_namespace(namespace)
            return True
        except client.ApiException as e:
            if e.status == 404:
                return False
            raise K8sClientException(exception=e)


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


    def delete_namespace(self, namespace):
        try:
            self._v1.delete_namespace(namespace)
        except client.ApiException as e:
            raise K8sClientException(
                msg=f"Failed to delete namespace '{namespace}'",
                exception=e
            )
        for _ in range(10):
            for _ in range(10):
                if not self.namespace_exists(namespace):
                    return
                time.sleep(0.6)
            print("Still deleting...")
        raise K8sClientException(
                msg=f"Failed to delete namespace '{namespace}'. The namespace still exists."
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


    def create_private_registry(self, namespace):
        ok, result = run_cmd(f"NAMESPACE={namespace} ./scripts/add_private_registry.sh")
        if not ok:
            raise K8sClientException(
                msg=f"Could not create private registry secret: {result}."
            )


    def install_operator(self):
        ok, result = run_cmd(
            "cd kube-awi; "
            "make install; "
            "IMG=229451923406.dkr.ecr.us-west-2.amazonaws.com/ausm/kube-awi:0.1 make deploy"
        )
        if not ok:
            raise K8sClientException(
                msg=f"Could not deploy the k8s operator: {result}."
            )


    def get_public_ip(self, namespace):
        try:
            svc = self._v1.read_namespaced_service("envoy-proxy", namespace)
        except client.ApiException as e:
            raise K8sClientException(
                msg=f"Failed to get envoy-proxy service details",
                exception=e
            )
        svc_ingress = svc.status.load_balancer.ingress
        if len(svc_ingress) == 0:
            raise K8sClientException(
                msg=f"Failed to obtain public address of envoy-proxy service. "
                "missing status.load_balancer.ingress[0]"
            )
        if svc_ingress[0].hostname is not None:
            return svc_ingress[0].hostname
        return svc_ingress[0].ip
