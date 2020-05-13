from pathlib import Path


def read_args(args, cli_config):
    """
    Parses args into the paramters needed to run script.
    Reads the specified host list file into a list.
    :param args: ArgumentParser() object from argparse
    :param cli_config:  GuiConfig() object
    :return: dictionary with the keys expected by the result data script
    """
    if args.config is not None:
        cli_config.load(Path(args.config))
    if args.log is not None:
        cli_config.config_dict['log_file'] = args.log
    if args.url is not None:
        cli_config.config_dict['sonarr_api_url'] = args.url
    if args.key is not None:
        cli_config.config_dict['sonarr_api_key'] = args.key
    if args.char is not None:
        cli_config.config_dict['replacement_char'] = args.char
    if args.new is not None:
        cli_config.config_dict['new_root'] = args.new
    if args.preview is True:
        cli_config.config_dict['preview'] = True
    if args.replace_space is True:
        cli_config.config_dict['replace_space'] = True
    if args.replace_root is True:
        cli_config.config_dict['replace_root'] = True
    if args.use_language_in_path is True:
        cli_config.config_dict['use_language_in_path'] = True

    return cli_config
