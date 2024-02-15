import os

from envparse import env

class Configuration():
    @classmethod
    def initialize(cls):
        """
        Creates helper for the script and loads environment variables.
        """
        cls._helper = {}

        cls.bool_env(
            'AWI_ENABLE_UI',
            default=True,
            help='Setting - If set to false, the UI application will not be created',
        )
        cls.bool_env(
            'AWI_ENABLE_K8S_OPERATOR',
            default=True,
            help='Setting - If set to false, the kube awi operator will not be created',
        )
        cls.str_env(
            'AWI_K8S_NAMESPACE',
            default='awi-system',
            help='Setting - The namespace, where AWI system will be installed',
        )
        cls.str_env(
            'AWI_K8S_CONTROLLER_CTX_FILE',
            default=os.path.expandvars('$HOME/.kube/config'),
            help='Setting - The kube config file for the cluster, where AWI will be installed',
        )
        cls.bool_env(
            'AWI_K8S_PURGE',
            default=False,
            help='Setting - If set to true, the script will clean up the namespace before installing AWI',
        )
        cls.str_env(
            'AWI_VMANAGE_USERNAME',
            default='',
            help='VManage - Username for VManage SDK Client',
        )
        cls.str_env(
            'AWI_VMANAGE_PASSWORD',
            default='',
            help='VManage - Password for VManage SDK Client',
        )
        cls.str_env(
            'AWI_K8S_CTX_FILE',
            default=os.path.expandvars('$HOME/.kube/config'),
            help='Controller - K8s config file containing context for accessing cluster',
        )
        cls.str_env(
            'AWI_AWS_CREDENTIALS_FILE',
            default=os.path.expandvars('$HOME/.aws/credentials'),
            help='Controller - AWS Credentials for accessing AWS resources',
        )
        cls.str_env(
            'AWI_GCP_CREDENTIALS_FILE',
            default='',
            help='Controller - [UNSUPPORTED] GCP Credentials for accessing GCP resources',
        )
        cls.str_env(
            'AWI_GOOGLE_MAPS_API_KEY',
            default='',
            help='UI - API Key for accessing Google Maps',
        )
        cls.str_env(
            'AWI_IP2LOCATION_API_KEY',
            default='',
            help='UI - API Key for accessing geological data',
        )

    @classmethod
    def str_env(cls, key, default, help):
        cls._env("str", key, default, help)

    @classmethod
    def bool_env(cls, key, default, help):
        cls._env("bool", key, default, help)

    @classmethod
    def _env(cls, attr, key, default, help):
        setattr(cls, key, getattr(env, attr)(key, default=default))
        cls._helper[key] = {
            "default": default,
            "help": help
        }

    @classmethod
    def print_help(cls):
        print("The script for AWI Installation.")
        print("To configure it, set the environment variables.")
        print("")
        for key in cls._helper:
            print(f"{key}\t{cls._helper[key]['help']}\n\tDefault: {cls._helper[key]['default']}")
