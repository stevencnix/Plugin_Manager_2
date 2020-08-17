from configparser import ConfigParser
from distutils.version import StrictVersion


class Plugin(object):

    def __init__(self, plugin_name, plugin_path):
        self.__details = ConfigParser()
        self.__name = plugin_name
        self.__path = plugin_path
        self.__ensure_details_defaults_are_backwards_compatible()

        # variables for stuff created during the plugin lifetime
        self.plugin_object = None
        self.error = None

    def __ensure_details_defaults_are_backwards_compatible(self):
        """
        Internal helper function.
        """
        if not self.details.has_option("Documentation", "Author"):
            self.author = "Unknown"
        if not self.details.has_option("Documentation", "Version"):
            self.version = "0.0"
        if not self.details.has_option("Documentation", "Website"):
            self.website = "None"
        if not self.details.has_option("Documentation", "Copyright"):
            self.copyright = "Unknown"
        if not self.details.has_option("Documentation", "Description"):
            self.description = ""

    @property
    def details(self):
        return self.__details

    @details.setter
    def details(self, config_details):
        """
        Fill in all details by storing a ``ConfigParser`` instance.

        .. warning::
            The values for ``plugin_name`` and
            ``plugin_path`` given a init time will superseed
            any value found in ``cfDetails`` in section
            'Core' for the options 'Name' and 'Module' (this
            is mostly for backward compatibility).
        """
        bkp_name = self.__name
        bkp_path = self.__path
        self.__details = config_details
        self.__name = bkp_name
        self.__path = bkp_path
        self.__ensure_details_defaults_are_backwards_compatible()

    @property
    def name(self):
        return self.details.get("Core", "Name")

    @name.setter
    def name(self, name):
        if not self.details.has_section("Core"):
            self.details.add_section("Core")
        self.details.set("Core", "Name", name)

    @property
    def path(self):
        return self.details.get("Core", "Module")

    @path.setter
    def path(self, path):
        if not self.details.has_section("Core"):
            self.details.add_section("Core")
        self.details.set("Core", "Module", path)

    @property
    def version(self):
        return StrictVersion(self.details.get("Documentation", "Version"))

    @version.setter
    def version(self, vstring):
        """
        Set the version of the plugin.

        Used by subclasses to provide different handling of the
        version number.
        """
        if isinstance(vstring, StrictVersion):
            vstring = str(vstring)
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Version", vstring)

    @property
    def author(self):
        return self.details.get("Documentation", "Author")

    @author.setter
    def author(self, author):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Author", author)

    @property
    def copyright(self):
        return self.details.get("Documentation", "Copyright")

    @copyright.setter
    def copyright(self, copyright_txt):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Copyright", copyright_txt)

    @property
    def website(self):
        return self.details.get("Documentation", "Website")

    @website.setter
    def website(self, website):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Website", website)

    @property
    def description(self):
        return self.details.get("Documentation", "Description")

    @description.setter
    def description(self, description):
        if not self.details.has_section("Documentation"):
            self.details.add_section("Documentation")
        self.details.set("Documentation", "Description", description)
