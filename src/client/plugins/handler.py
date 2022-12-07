import pathlib
import importlib
import logging

def load_plugins():
    for plugin in pathlib.Path(f'{pathlib.Path(__file__).resolve().parent}/src/').glob('*.py'):
        try:
            importlib.import_module(f'plugins.src.{plugin.name[:-3]}').init()
        except AttributeError:
            logging.critical(f'Plugin "{plugin.name[:-3]}" did not provide an init() function')
            