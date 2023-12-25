"""
This module gives you access to the encrypted config.json file.

This is the only way to access parts of the config file. The plugins
are only allowed to access THEIR configuration.

Exposed functions:
    - get_plugin_config
"""

from typing import Dict, Any

import logging

from utils import stack
from utils import constants


def _get_plugin_name(depth: int = 3) -> str:
    return stack.get_caller(depth)[0].split('plugins.', 1)[1].split('.', 1)[0]


def get_plugin_config() -> Dict[str, Any]:
    """
    Return the configuration of the caller plugin.

    Returns:
        Dict[Any, Any]: Returns a json (dictionary) object containing
                        all the configurations for the plugin.
    """
    plugin_name = _get_plugin_name()
    plugins = constants.CONFIG.get('plugins')
    if not plugins:
        logging.critical('Invalid config: no plugin section')
        return {}

    plugin_config = plugins.get(plugin_name)
    if not plugin_config:
        logging.warning(f'Empty plugin setting for plugin "{plugin_name}"')
        return {}

    return plugin_config  # type: ignore[no-any-return]
