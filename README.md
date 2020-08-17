# Plugin Manager 2.0

## About Plugin Manager 2.0

Plugin Manager 2.0 is a simple Python library I created based off of Thibauld Nion's yapsy. 
I liked how yapsy uses a config file in conjunction with a python module for locating and describing.
My plugin manager does not have the robustness and customizability that yapsy has. It is meant to be a very simple
ready to go hands of plugin manager.

## Usage

1. Initialize the plugin manager

	``` shell
	plugin_manager = PluginManager(plugin_folder=\<INSERT PLUGINS DIR PATH HERE\>)
	```
	
2. Import the plugins in the plugins directory

	``` shell
	plugin_manager.import_plugins()
	```
 
3. Get the imported plugin

	```shell
	plugin = plugin_manager.get_active_plugin("Plugin name")
	```
 
    or

    ```shell
    plugins = plugin_manager.active_plugins
    ```
