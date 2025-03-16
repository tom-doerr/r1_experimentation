import inspect  # Standard library imports
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Generator, List

import litellm  # Third-party library imports

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'
litellm.model = FLASH  # Set the default model directly. Ensure this is used as the default.
litellm.model_list = [{
    "model_name": "default",
    "litellm_params": {
        "model": FLASH,
    }
}]

import shlex  # Standard library imports
import subprocess

import litellm  # Third-party library imports


FLASH: str = 'openrouter/google/gemini-2.0-flash-001'
