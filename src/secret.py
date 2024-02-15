import base64
import os
from typing import Union

def _base64encode(input: Union[str, bytes]) -> str:
    if isinstance(input, str):
        input = input.encode("utf-8")
    return base64.b64encode(input).decode("utf-8")


def _base64encodeFile(filename: str) -> str:
    try:
        with open(os.path.expandvars(filename), 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        return ""
    return _base64encode(data)


def apply_secrets(k8s_client, awi_config):
    k8s_client.apply_template_manifest(
        "templates/secrets.tmpl",
        {
            "VMANAGE_USERNAME": _base64encode(awi_config.AWI_VMANAGE_USERNAME),
            "VMANAGE_PASSWORD": _base64encode(awi_config.AWI_VMANAGE_PASSWORD),
            "K8S_CTX": _base64encodeFile(awi_config.AWI_K8S_CTX_FILE),
            "AWS_CREDS": _base64encodeFile(awi_config.AWI_AWS_CREDENTIALS_FILE),
            "GCP_CREDS": _base64encodeFile(awi_config.AWI_GCP_CREDENTIALS_FILE),
            "GOOGLE_MAPS_API_KEY": _base64encode(awi_config.AWI_GOOGLE_MAPS_API_KEY),
            "IP2LOCATION_API_KEY": _base64encode(awi_config.AWI_IP2LOCATION_API_KEY),
        }
    )
