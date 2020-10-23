
import logging
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

DB = SQLAlchemy()

MA = Marshmallow()

LOG = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).absolute().parent.parent.parent
DEFAULT_CONFIG_FILE = ROOT_DIR / "config/config.toml"