"""
    Extending Flask for loading config file
"""

import yaml
from flask import Config as BaseConfig
from flask import Flask as BaseFlask


class Config(BaseConfig):
    """Flask config enhanced with a `from_yaml` method."""

    def from_yaml(self, config_file):
        """Convert YAML file value in Key-Value pair.
        Args:
            config_file (string): current file path
        """

        with open(config_file) as file:
            config_values = yaml.safe_load(file)

        for key in config_values.keys():
            self[key] = config_values[key]


class Flask(BaseFlask):
    """Extended version of `Flask` that implements custom config class."""

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)
