import sys

from src.configuration import Configuration as awi_config
from src.k8s import K8sClient
from src.secret import apply_secrets

print("Loading AWI Configuration.")
awi_config.initialize()
print("Done.")

if "-h" in sys.argv or "--help" in sys.argv:
    awi_config.print_help()
    exit(0)

print("Loading K8s Client.")
client = K8sClient()
print("Done.")

print("Generating and applying k8s secrets.")
apply_secrets(client, awi_config)
print("Done.")
