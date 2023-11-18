"""Module providing a function for parsing config"""
import configparser


class ConfigUtil:
    """Class representing a util"""

    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section, option, fallback=None):
        """Function to get"""
        return self.config.get(section, option, fallback=fallback)

    def getint(self, section, option, fallback=None):
        """Function to getint"""
        return self.config.getint(section, option, fallback=fallback)

    def getfloat(self, section, option, fallback=None):
        """Function to getfloat"""
        return self.config.getfloat(section, option, fallback=fallback)
