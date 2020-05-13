import yaml
from pathlib import Path


class GuiConfig(object):
    """
    Class for program configuration.
    """
    def __init__(self, config_file=None, output_queue=None):
        self.config_file = None
        self.config_dict = None
        self.output_queue = output_queue
        self.config_dict = self.__default__
        if config_file is not None:
            self.load(config_file)
        self.logger = None
        self.gui_queue = None
        self.runner_queue = None


    @property
    def __default__(self):
        """
        return configuration defaults
        :return: dict
        """
        return {
            'sonarr_api_url': None,
            'sonarr_api_key': None,
            'new_name_components': [
                ('title', True),
                (' (', False),
                ('year', True),
                (')', False),
            ],
            'replace_space': True,
            'replacement_char': '_',
            'log_file': 'rename.log',
            'replace_root': False,
            'new_root': None,
            'preview': False,
            'use_language_in_path': True,

        }

    def __load_yml__(self):
        """
        load the yaml file to dict
        :return: dict
        """
        try:
            yml_file = self.config_file.read_text('utf-8')
            config_file_dict = yaml.load(yml_file, Loader=yaml.FullLoader)
        except (FileNotFoundError, yaml.scanner.ScannerError):
            config_file_dict = {}
            if self.output_queue is not None:
                self.output_queue.put(('ERROR: configuration file:' + str(self.config_file.name) +
                                       'could not be loaded. Using defaults', 8))
            else:
                print('configuration:', self.config_file.name, 'could not be loaded')
        return config_file_dict

    def update_from_gui(self, parameters):
        """
        Map parameters dict to configuration dict
        :param parameters: dict
        :return: None
        """
        for element in parameters:
            self.config_dict[element] = parameters[element]

    def merge_config(self, config_local):
        """
        Merge configuration changes into the current configuration.
        This way the user doesn't have to write the entire configuration.
        :param config_local: dict
        :return:
        """
        for element in config_local:
            self.config_dict[element] = config_local[element]
        print(self.config_dict)

    def save(self, config_path=None):
        """
        Dumps configuration to file
        :param config_path: pathlib.Path()
        :return: None
        """
        if config_path is not None:
            self.config_file = config_path
        output = yaml.dump(self.config_dict)
        self.config_file.write_text(output, encoding='utf-8')

    def load(self, config_file=None):
        """
        Loads configuration from file and merges it to config dict
        :param config_file: pathlib.Path()
        :return: None
        """
        self.config_file = config_file
        if self.config_dict is None:  # set default values if no defaults are specified
            self.config_dict = self.__default__

        if self.config_file is not None:
            config_local = self.__load_yml__()
        else:
            config_local = {}
        self.merge_config(config_local)

    def get(self, element):
        """
        return element from configuration dict
        :param element: str used as key for config_dict
        :return: value from config_dict
        """
        return self.config_dict[element]

    @property
    def log_path(self):
        return Path(self.config_dict['log_file'])

