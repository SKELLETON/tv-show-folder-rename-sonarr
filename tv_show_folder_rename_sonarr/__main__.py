from tv_show_folder_rename_sonarr.run_gui import run_gui
from tv_show_folder_rename_sonarr.run_cli import run_cli


def main(mode='m'):
    if mode == 'c':
        run_cli()
    else:
        run_gui()


if __name__ == '__main__':
    main(mode='m')


        


