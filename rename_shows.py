from tv_show_folder_rename_sonarr.__main__ import main
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # run GUI
        main(mode='m')
    else:
        # run CLI
        main(mode='c')