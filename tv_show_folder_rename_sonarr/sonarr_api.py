import requests


class SonarrApi(object):

    def __init__(self, config):
        self.config = config

    def get_all_shows(self):
        request_url = self.config.get('sonarr_api_url') + '/series?apikey=' + self.config.get('sonarr_api_key')
        response = requests.get(request_url)
        return response.json()

    def get_show(self, id):
        request_url = self.config.get('sonarr_api_url') + '/series/' + str(id) + '?apikey=' + self.config.get('sonarr_api_key')
        response = requests.get(request_url)
        return response.json()

    def get_all_language_profiles(self):
        request_url = self.config.get('sonarr_api_url') + '/v3/languageprofile?apikey=' + self.config.get('sonarr_api_key')
        response = requests.get(request_url)
        return response.json()

    def update_show(self, show_details):
        request_url = self.config.get('sonarr_api_url') + '/series?apikey=' + self.config.get('sonarr_api_key')
        response = requests.put(request_url, json=show_details)
        return  response.status_code
