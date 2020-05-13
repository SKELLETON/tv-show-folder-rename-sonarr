from tv_show_folder_rename_sonarr.logger import Logger
from tv_show_folder_rename_sonarr.config import GuiConfig
from tv_show_folder_rename_sonarr.cli_helpers import read_args
from tv_show_folder_rename_sonarr.rename_shows import run_rename
from pathlib import Path
import argparse


def run_cli():
    """
    Runs the cli interface. Requires that the script was called with proper arguments. Accesses sys.argv for arguments.
    Starts worker script after parsing inputs.
    :return: None
    """
    cli_default_config = Path('config.yml')
    cli_config = GuiConfig(cli_default_config)
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify configuration file to load", default=None)
    parser.add_argument("-l", "--log", help="Specify log file.", default=None, )
    parser.add_argument("-u", "--url", help="Specify the Sonarr API url.", default=None, )
    parser.add_argument("-k", "--key", help="Specify the Sonarr API key", default=None, )
    parser.add_argument("--char", help="replacement char for space", default=None, )
    parser.add_argument("-n", "--new", help="new library root path", default=None, )

    parser.add_argument("-p", "--preview", help="Switch use if you want to preview the changes",
                        default=False, action='store_true')
    parser.add_argument("--replace_space", help="Switch use if you want to replace the space char in the folder name",
                        default=False, action='store_true')
    parser.add_argument("--replace_root", help="Switch use if you want to change the root folder of your library",
                        default=False, action='store_true')
    parser.add_argument("--use_language_in_path", help="Switch use if you want to use the language of a show in the library path",
                        default=False, action='store_true')

    args = parser.parse_args()
    cli_config = read_args(args, cli_config)
    cli_config.logger = Logger(log_file=Path(cli_config.get('log_file')))
    run_rename(cli_config)
