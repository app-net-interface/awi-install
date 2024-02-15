import sys

from src.configuration import Configuration as awi_config
from src.k8s import K8sClient
from src.secret import apply_secrets
from validate import validate_tools

print("Loading AWI Configuration.")
awi_config.initialize()
print("Done.")

if "-h" in sys.argv or "--help" in sys.argv:
    awi_config.print_help()
    exit(0)

print("Loading K8s Client.")
client = K8sClient()
print("Done.")

validate_tools()

print(f"Checking if {awi_config.AWI_K8S_NAMESPACE} namespace exists.")
if client.namespace_exists(awi_config.AWI_K8S_NAMESPACE):
    if not awi_config.AWI_K8S_PURGE:
        print(
            f"Error: The namespace '{awi_config.AWI_K8S_NAMESPACE}' already exists. "
            "If you want to purge it and start again, run the script "
            "with environment variable AWI_K8S_PURGE=true"
        )
        exit(1)
    print("Exists. The removal of it and its subresources in progress.")
    client.purge_namespace(awi_config.AWI_K8S_NAMESPACE)
    print("Done.")
else:
    print(f"The {awi_config.AWI_K8S_NAMESPACE} namespace doesn't exist.")

print(f"Creating {awi_config.AWI_K8S_NAMESPACE} namespace.")
client.create_namespace(awi_config.AWI_K8S_NAMESPACE)
print("Done.")

print("Creating credentials for private registry.")
client.create_private_registry(awi_config.AWI_K8S_NAMESPACE)
print("Done.")

print("Generating and applying k8s secrets.")
apply_secrets(client, awi_config)
print("Done.")

print("Applying the manifest.")
client.apply_manifest("manifests/awi.yaml")
print("Done.")

# TODO: Fix kube-awi to allow specifying different namespace than awi-system
if awi_config.AWI_ENABLE_K8S_OPERATOR:
    print("Deploying the k8s operator.")
    client.install_operator()
    print("Done.")


print(client.get_public_ip(awi_config.AWI_K8S_NAMESPACE))

