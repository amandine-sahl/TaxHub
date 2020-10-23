
import os
import secrets
import toml
from marshmallow import (
    Schema,
    fields,
    validates_schema,
    ValidationError,
    post_load,
)
from marshmallow.validate import OneOf, Regexp, Email
from pathlib import Path

from app.utils.env import DEFAULT_CONFIG_FILE


def load_and_validate_toml(toml_file, config_schema):
    """
        Fonction qui charge un fichier toml
         et le valide avec un Schema marshmallow
    """
    if Path(toml_file).is_file():
        toml_config = load_toml(toml_file)
        try:
            configs_py = config_schema().load(toml_config)
        except Exception as configerrors:
            raise Exception(f"Configuration error {toml_file}, {configerrors}")            
        return configs_py
    else:
        raise Exception(f"Missing file {toml_file}")


def load_toml(toml_file):
    """
        Fonction qui charge un fichier toml
    """
    if Path(toml_file).is_file():
        toml_config = toml.load(str(toml_file))
        return toml_config
    else:
        raise Exception("Missing file {}".format(toml_file))


class TaxhubConfig(Schema):

    # API CONFIGURATION
    OPENAPI_VERSION = fields.String(missing="3.0.2")
    OPENAPI_URL_PREFIX = fields.String(missing="/api")
    OPENAPI_SWAGGER_UI_PATH = fields.String(missing="/swagger")
    OPENAPI_SWAGGER_UI_VERSION = fields.String(missing="3.24.2")
    OPENAPI_SWAGGER_UI_URL = fields.String(
        missing="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    )
    OPENAPI_REDOC_PATH = fields.String(missing="/redoc")
    OPENAPI_REDOC_URL = fields.String(
        missing="https://cdn.jsdelivr.net/npm/redoc@2.0.0-rc.30/bundles/redoc.standalone.js"
    )
    API_VERSION = fields.String(missing="v1")
    API_TITLE = fields.String(missing="API de l'application Taxhub")

    # APPLI CONFIGURATION
    COOKIE_EXPIRATION = fields.Integer(missing=3600)
    PASS_METHOD = fields.String(missing="hash")
    COOKIE_AUTORENEW = fields.Boolean(missing=True)
    TRAP_ALL_EXCEPTIONS = fields.Boolean(missing=False)

    SECRET_KEY = fields.String(missing=secrets.token_hex(32))

    SQLALCHEMY_DATABASE_URI = fields.String(
        required=True,
        # validate=Regexp(
        #     "^postgresql:\/\/.*:.*@[^:]+:\w+\/\w+$",
        #     0,
        #     "Database uri is invalid ex: postgresql://monuser:monpass@server:port/db_name",
        # )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = fields.Boolean(missing=False)


def load_config(config_file=DEFAULT_CONFIG_FILE):
    """ Load the  configuration from a given file """
    # load and validate configuration
    configs_py = load_and_validate_toml(
        config_file, TaxhubConfig
    )
    return configs_py
