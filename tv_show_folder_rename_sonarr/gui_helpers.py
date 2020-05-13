
def update_window_from_config(window_var, config, values, file_name):
    """
    Load configuration from file and update GUI elements
    :param window_var: simplepygui window
    :param config: GuiConfig() object
    :param values: dict current GUI inputs
    :param file_name: pathlib.Path()
    :return: GuiConfig()
    """
    config.update_from_parameters(values)
    config.load(file_name)
    for element in config.config_dict:
        window_var[element].update(config.get(element))
    return config


def save_config(config, logger, values, file_name=None):
    """
    Save configuration to file
    :param config: GuiConfig()
    :param logger: Logger()
    :param values: current GUI inputs
    :param file_name: pathlib.Path() file that the configuration is saved to
    :return: None
    """
    config.update_from_gui(values)
    if file_name is not None:
        config.save(file_name)
    else:
        config.save()
    logger.log('Saved configuration file: ' + str(config.config_file.name), 0)
