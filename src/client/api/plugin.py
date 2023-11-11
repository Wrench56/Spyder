"""
This module is for plugins to make themselves public for other plugins.

Exposed functions:
    - register
    - unregister
    - get
    - exists
"""

from typing import Dict, Optional
import logging

from plugins import base_plugin


_plugins: Dict[str, base_plugin.Plugin] = {}

def register(name: str, plugin: base_plugin.Plugin) -> bool:
    """
    Register a plugin

    Args:
        name: Name of the plugin. Others can access the plugin
              through this name.
        plugin: The plugin object itself

    Returns:
        bool: True if the plugin was registered successfully, else False
    """
    if name not in _plugins:
        _plugins[name] = plugin
        return True

    logging.error(f'Plugin with name "{name}" already registered')
    return False

def unregister(name: str) -> bool:
    """
    Un-register a plugin

    Args:
        name: Name of the plugin to unregister
    Returns:
        bool: True if the plugin was unregistered successfully
              and else False
    """
    if name in _plugins:
        del _plugins[name]
        return True

    logging.error(f'Plugin "{name}" cannot be unregistered as it never was registered')
    return False


def get(name: str) -> Optional[base_plugin.Plugin]:
    """
    Return a plugin by name

    Args:
        name: Name of the plugin
    Returns:
        Plugin: Returns the plugin object itself
    """
    if name in _plugins:
        return _plugins[name]

    logging.error(f'The plugin {name} you tried to get does not exist')
    return None

def exists(name: str) -> bool:
    """
    Check whether the a plugin is registered

    Args:
        name: Name of the plugin
    Returns:
        bool: True if the plugin exists, else False
    """
    if name in _plugins:
        return True
    return False
