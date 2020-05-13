import queue
import threading
import PySimpleGUI as sg
from pathlib import Path
from tv_show_folder_rename_sonarr.rename_shows import run_rename
from tv_show_folder_rename_sonarr.config import GuiConfig
from tv_show_folder_rename_sonarr.gui_layout import get_layout
from tv_show_folder_rename_sonarr.logger import Logger
import tv_show_folder_rename_sonarr.gui_helpers as gui_helpers


def run_gui():
    """
    Gui main loop, initiates the queues and the logger, starts the gui, reacts to events.
    :return: None
    """

    gui_queue = queue.Queue()  # queue used to communicate between the gui and the threads
    log_queue = queue.Queue()
    runner_queue = queue.Queue()

    logger = Logger(gui_queue=log_queue)

    default_config = Path('config.yml')
    config = GuiConfig(default_config)
    logger.file = config.log_path
    config.logger = logger
    config.gui_queue = gui_queue
    config.runner_queue = runner_queue
    window = sg.Window('Sonarr Show Folder Renamer', get_layout(config))

    # --------------------- EVENT LOOP ---------------------
    while True:
        event, values = window.read(timeout=10)
        if event in (None, 'Exit'):
            break
        elif event.startswith('Run'):
            window['Run'].update(disabled=True)
            window['Stop'].update(disabled=False)
            config.update_from_gui(values)
            config.logger.file = config.log_path
            window['progress'].update_bar(0, 100)

            threading.Thread(target=run_rename, args=([config]), daemon=True).start()
        elif event == 'Stop':
            window['Stop'].update(disabled=True)
            logger.log('Stopping runner', 8)
            runner_queue.put('stop')
        elif event == 'Save::config':
            gui_helpers.save_config(config, logger, values)
        elif event == 'Save As::config':
            file_name = sg.popup_get_file('Save Configuration As', save_as=True, no_window=True,
                                          file_types=(('Configuration Files', '*.yml'),))
            if file_name != '':
                gui_helpers.save_config(config, logger, values, Path(file_name))
        elif event == 'Load::config':
            file_name = sg.popup_get_file('Select Configuration File', no_window=True,
                                          file_types=(('Configuration Files', '*.yml'),))
            if file_name != '':
                logger.log('Loading configuration from ' + str(file_name), 2)
                config = gui_helpers.update_window_from_config(window, config, values, Path(file_name))
                logger.file = Path(config.get('log_file'))

        # --------------- Check for incoming messages from threads  ---------------
        try:
            message = gui_queue.get_nowait()
        except queue.Empty:  # get_nowait() will get exception when Queue is empty
            message = None  # break from the loop if no more messages are queued up

        # if message received from gui queue, update display elements
        if message:
            level = message[1]
            if level == 100:  # level 100 is enable element
                window[message[0]].update(disabled=False)
            elif level == 101:  # level 101 disable element
                window[message[0]].update(disabled=True)
            elif level == 104:
                window['progress'].update_bar(message[0] + 1)

        # show log in the "display" text field
        logger.display(window.FindElement('display'), mode='tk')

    # if user exits the window, then close the window and exit the GUI func
    window.close()