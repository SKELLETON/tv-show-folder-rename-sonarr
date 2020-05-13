from datetime import date
import PySimpleGUI as sg


def get_layout(config):
    """
    Defines the layout of the GUI. Sets defaults according to configuration
    :param config: GuiConfig()
    :return: List()
    """

    menu_def = [
        ['Configuration', ['Load::config', 'Save::config', 'Save As::config']],
    ]

    column_1 = [
        [sg.Text('Sonarr API URL', size=(15, 1)), sg.InputText(config.get('sonarr_api_url'), key='sonarr_api_url')],
        [sg.Text('Sonarr API Key', size=(15, 1)), sg.InputText(config.get('sonarr_api_key'), key='sonarr_api_key')],
        [sg.Checkbox('replace_space', default=config.get('replace_space'), key='replace_space')],
        [sg.Text('replacement_char', size=(15, 1)),
         sg.InputText(config.get('replacement_char'), key='replacement_char', size=(3, 1))],
        [sg.Text('log_file', size=(15, 1)), sg.InputText(config.get('log_file'), key='log_file')],
        [sg.Checkbox('replace_root', default=config.get('replace_root'), key='replace_root')],
        [sg.Text('new_root', size=(15, 1)), sg.InputText(config.get('new_root'), key='new_root')],
        [sg.Checkbox('preview', default=config.get('preview'), key='preview')],
        [sg.Checkbox('use_language_in_path', default=config.get('use_language_in_path'), key='use_language_in_path')],
    ]

    column_3 = [
        [sg.Multiline(size=(70, 25), key='display', autoscroll=True)]
    ]

    layout = [
        [sg.Menu(menu_def, )],
        [sg.Column(column_1), sg.Column(column_3)],
        [sg.Button('Run', key='Run'),
         sg.Button('Stop', key='Stop', disabled=True),
         sg.ProgressBar(1, orientation='h', size=(60, 20), key='progress')],
    ]
    return layout
