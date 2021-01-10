import yaml


class ConfigLoader:
    """
    Utility class for loading system configurations, processing yaml configuration files and returns configurations in internal dictionary representations.
    """

    def __init__(self, config_path=None):
        if config_path:
          self.config_path = config_path
        else:
            self.config_path = "../../configs/"

    
