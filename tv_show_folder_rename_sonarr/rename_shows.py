from tv_show_folder_rename_sonarr.sonarr_api import SonarrApi
from pathlib import  Path
import queue


def stop_rename(config):
    """
    Checks runner_queue if the user asked to interrupt the loop
    :param config: GuiConfig
    :return: bool True if message to stop was received
    """
    if config.runner_queue is not None:
        try:
            message = config.runner_queue.get_nowait()
        except queue.Empty:  # get_nowait() will get exception when Queue is empty
            message = None  # break from the loop if no more messages are queued up
    else:
        message = None

    if message == 'stop':
        print('received stop')
        config.logger.log('Rename of Series folders has been aborted by user', 7)
        config.gui_queue.put(('Stop', 101))
        config.gui_queue.put(('Run', 100))
        return True
    else:
        return False


def run_rename(config):
    connection = SonarrApi(config)
    language_profiles_json = connection.get_all_language_profiles()
    language_profiles = {}
    for element in language_profiles_json:
        language_profiles[element['id']] = str(element['name']).lower()
    config.logger.log('Getting list of all shows from Sonarr')
    shows = connection.get_all_shows()
    config.logger.log('Starting to loop through shows')
    if stop_rename(config) is True:
        return
    for show in shows:
        if stop_rename(config) is True:
            return
        show_id = show['id']
        config.logger.log('Working on show_id ' + str(show_id))
        show_details = connection.get_show(show_id)
        show_path = Path(show_details['path'])
        new_path = get_new_path(config, show_path, show_details, language_profiles)
        if config.get('preview') is False:
            if not new_path.exists():
                show_path.rename(new_path)
                show_details['path'] = str(new_path)
                result = connection.update_show(show_details)
                config.logger.log('Moved show to "' + str(new_path) + '". Sonarr update response was: ' + str(result))
            else:
                config.logger.log('Path "' + str(new_path) + '" already exists. Skipping moving and updating the show',
                                  8)
        else:
            config.logger.log('Preview run. New path for show would be: ' + str(new_path))
    config.logger.log('Finished renaming the tv shows known to sonarr')
    if config.gui_queue is not None:
        config.gui_queue.put(('Stop', 101))
        config.gui_queue.put(('Run', 100))


def get_new_path(config, show_path, show_details, language_profiles):
    new_name = ''
    for element in config.get('new_name_components'):
        if element[1] is True:
            new_name += str(show_details[element[0]])
        else:
            new_name += element[0]

    # Make the names windows friendly, in case i check via smb share
    illegal_chars = ['/', '\\', ':', '?', '*']
    for illegal_char in illegal_chars:
        new_name = new_name.replace(illegal_char, ' ')
    new_name = " ".join(new_name.split())

    # some shows already have the year in the title
    # check if year is duplicated -- will only work if the new name is supposed to end with ' (year)'
    show_name_no_year = new_name[:-7]
    year = new_name[-7:]
    if show_name_no_year.endswith(year):
        new_name = show_name_no_year

    # perform space replacement if required
    if config.get('replace_space') is True:
        new_name = new_name.replace(' ', config.get('replacement_char'))

    if config.get('replace_root') is True:
        new_path = Path(config.get('new_root'))
    else:
        new_path = show_path.parent

    if config.get('use_language_in_path') is True:
        lang_id = show_details['languageProfileId']
        new_path = new_path / language_profiles[lang_id]

    new_path = new_path / new_name
    return new_path
