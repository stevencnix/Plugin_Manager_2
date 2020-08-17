import importlib
import importlib.util
import logging
import pathlib
import sys
import inspect
from configparser import ConfigParser
from plugin import Plugin


class PluginManager:
    """
    A basic python plugin manager based off of https://gist.github.com/mepcotterell/6004997
    Rewritten using ImportLib and pathlib and updated to Python 3
    This will allow users to make plugin folders place any number of plugins in them, grab the module and then
    using getattr initialize and object from that module
    """

    def __init__(self, plugin_folder: str, plugin_info_ext="info", log=logging):
        """
        This is the initialization method. User must set the plugin folder location. They can also set their own logging
        should they have their own. Finally they can also set the max number of lodable plugins if they want.
        :param plugin_folder: Base dir for plugins.
        :param log: Python logging.
        :param max_loaded_plugins: The max number of loadable plugins.
        """
        self.__logging = log
        self.__plugin_folders = pathlib.Path(plugin_folder)
        self.__plugin_config_ext = plugin_info_ext
        self.__imported_plugins = dict()

        # !!!IMPORTANT: This line insures that the plugin directory gets added to the path so that it can be seen.
        # if not included the plugins folder may not be detected.
        paths = [self.__plugin_folders]+[f for f in self.__plugin_folders.iterdir() if f.is_dir()]
        for path in paths:
            sys.path.append(path.as_posix())

    def import_plugins(self):
        for plugin_info_path in pathlib.Path(self.__plugin_folders).glob(f"**/*.{self.__plugin_config_ext}"):
            config_parser = ConfigParser()
            config_parser.read(plugin_info_path)
            try:
                if config_parser.get("Core", "Module"):
                    module_name = config_parser.get("Core", "Module")
                    module = importlib.import_module(module_name)
                    if module:
                        if config_parser.get("Core", "Name"):
                            plugin = Plugin(config_parser.get("Core", "Name"),
                                                     f"{plugin_info_path.parent}\\{module_name}.py")
                            plugin.details = config_parser
                            cls_name = [m[0] for m in inspect.getmembers(module, inspect.isclass) if
                                        m[1].__module__ == module.__name__]
                            _cls = getattr(module, cls_name[0])
                            plugin.plugin_object = _cls()

                            if plugin:
                                self.__imported_plugins[plugin.name] = plugin
                                self.__logging.info(f"{plugin.name} imported successfully.")
                    else:
                        self.__logging.warning(f"Missing Module for Plugin: {plugin_info_path.absolute().as_posix()}")
                else:
                    raise ValueError("Plugin Config file is missing necessary parameters.")
            except ModuleNotFoundError as me:
                self.__logging.warning(f"Missing Module for Plugin: {plugin_info_path.absolute().as_posix()}")

    def get_active_plugin(self, plugin_name: str):
        return self.__imported_plugins.get(plugin_name)

    def remove_plugin(self, plugin_name):
        """
        Removes a loaded plugin
        :param plugin_name: the name of the plugin to be removed
        :return: None
        """
        del self.__imported_plugins[plugin_name]
        self.__logging.info(f"{plugin_name} removed successfully.")

    @property
    def active_plugins(self):
        return self.__imported_plugins
