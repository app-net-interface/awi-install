import os

from envparse import env

class Configuration():
    @classmethod
    def initialize(cls):
        """
        Creates helper for the script and loads environment variables.
        """
        cls._helper = {}

        cls.str_env(
            'AWI_CATALYST_SDWAN_USERNAME',
            default='',
            help='Catalyst SDWAN - Username for Catalyst SDWAN SDK Client',
        )
        cls.str_env(
            'AWI_CATALYST_SDWAN_PASSWORD',
            default='',
            help='Catalyst SDWAN - Password for Catalyst SDWAN SDK Client',
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
    def _env(cls, attr, key, default, help):
        setattr(cls, key, getattr(env, attr)(key, default=default))
        cls._helper[key] = {
            "default": default,
            "help": help
        }

    @classmethod
    def print_help(cls):
        print("The script for generating secrets.")
        print("To configure it, set the environment variables.")
        print("")
        for key in cls._helper:
            print(f"{key}\t{cls._helper[key]['help']}\n\tDefault: {cls._helper[key]['default']}")
