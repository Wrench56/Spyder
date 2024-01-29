"""
This module is for the "plugin manager" plugin ONLY!

In this module there are functions to import and
manage extensions/plugins from another plugin. This API
module should be exposed to one plugin only, the "plugin manager"

Exposed functions:
    - import_plugin
"""

from typing import Optional
import importlib
import logging

from plugins.base_plugin import Plugin


def import_plugin(name: str) -> Optional[Plugin]:
    """
    Import a plugin with importlib and return the Plugin() object.

    Args:
        name: Name of the plugin

    Returns:
        None | Plugin: Returns Plugin() object if import was successful
                       else None
    """
    try:
        plugin: Plugin = importlib.import_module(f'plugins.{name}.src.main').init()
        return plugin
    except TypeError:
        # Abstract class (Plugin) does not implement methods like load & unload
        logging.error(f'Plugin "{name}" does not implement abstract methods')
    except AttributeError:
        # No init() function
        logging.error(f'Plugin "{name}" does not provide an init() function')
    except ModuleNotFoundError:
        # No such file
        logging.error(f'Plugin "{name}" does not exist')

    return None
