from typing import Optional
import importlib
import logging

from plugins.base_plugin import Plugin


def import_plugin(name: str) -> Optional[Plugin]:
    try:
        plugin: Plugin = importlib.import_module(f'plugins.{name}.main').init()
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
