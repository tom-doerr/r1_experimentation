from typing import Dict
from .config import DEFAULT_MODEL, global_settings
from .utils import normalize_model_name

DEFAULT_TIMEOUT = 10
MAX_COMMAND_LENGTH = 100

__all__ = ["DEFAULT_MODEL", "global_settings", "normalize_model_name"]

