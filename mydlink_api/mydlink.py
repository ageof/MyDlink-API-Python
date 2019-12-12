import datetime
import json
import time
import urllib.parse

from mydlink_api.utils.hashing import Hashing
from mydlink_api.utils.url import Url


class MyDlink:
    api_url = "https://api.auto.mydlink.com"
    client_id = "mydlinkuapandroid"
    android_id = "bd36a6c011f1287e"
    oauth_secret = "5259311fa8cab90f09f2dc1e09d2d8ee"

    def __init__(self, email: str, password: str, proxy=None):
        self.name = "PythonApi"
        self.email = email
        self.password = Hashing.md5Hashing(password)
        self.url_utils = Url(proxy)
        self.__login()

    def __login(self):
        oauth_sub_url = "/oauth/authorize"
        login_url = "{oauth_sub_url}?" \
                    "client_id={client_id}" \
                    "&redirect_uri={redirect_url_b64_encode}" \
                    "&user_name={email}" \
                    "&password={password}" \
                    "&response_type=token" \
                    "&timestamp={timestamp}" \
                    "&uc_id={android_id}" \
                    "&uc_name={name}".format(
            oauth_sub_url=oauth_sub_url,
            client_id=self.client_id,
            redirect_url_b64_encode=urllib.parse.quote("https://mydlink.com"),
            email=urllib.parse.quote(self.email),
            password=self.password,
            timestamp=str(time.time())[0:10],
            android_id=self.android_id,
            name=self.name
        )
        signatur = Hashing.md5Hashing(login_url + self.oauth_secret)
        request_url = "{api_url}{login_url}&sig={signatur}".format(
            api_url=self.api_url,
            login_url=login_url,
            signatur=signatur
        )

        response = self.url_utils.get_request(request_url)
        self.login_params = Url.get_params(response)

    def get_device_list(self) -> json:
        device_list_url = "https://{openapi}/me/device/list?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )
        response = self.url_utils.get_request(url=device_list_url, type=self.url_utils.TYPE_GET)
        device_list_json = Url.parse(response.content.decode('utf8'))
        return device_list_json['data']

    def get_device_details(self, mydlink_id: str, mac: str) -> json:
        device_detail_url = "https://{openapi}/me/device/info?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )
        json_object = {}
        json_object['mac'] = mac
        json_object['mydlink_id'] = mydlink_id

        json_object_list = []
        json_object_list.append(json_object)

        json_object_final = {}
        json_object_final['data'] = json_object_list

        response = self.url_utils.get_request(url=device_detail_url, type=self.url_utils.TYPE_POST,
                                              input_json=json_object_final)

        device_detail_json = Url.parse(response.content.decode('utf8'))
        return device_detail_json['data'][0]

    def get_mydlink_cloud_recordings(self, year: int, month: int, day: int):
        recording_date_start = datetime.datetime(year, month, day, 2, 00, 00)
        recording_date_end = datetime.datetime(year, month, day, 23, 59, 59, 999999)

        recording_timestampe_start = str(recording_date_start.timestamp()).replace(".", "") + "00"
        recording_timestampe_end = str(recording_date_end.timestamp()).replace(".", "")[0:13]

        event_list_meta_json = self.get_event_list_meta_infos(recording_timestampe_end, recording_timestampe_start)
        if 'path' in event_list_meta_json['data'][0]:
            response_all_events_details = self.url_utils.get_request(url=event_list_meta_json['data'][0]['path'],
                                                                     type=self.url_utils.TYPE_GET)
            all_events_details_json = Url.parse(response_all_events_details.content.decode('utf8'))
            all_events_details_json = all_events_details_json['data'][0]['data']
        else:
            all_events_details_json = event_list_meta_json['data'][0]['data']
        self.__get_mydlink_cloud_recordings_file(all_events_details_json)

    def get_event_list_meta_infos(self, recording_timestampe_end: int, recording_timestampe_start: int) -> json:
        device_detail_url = "https://{openapi}/me/nvr/event/list?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )

        json_object = {}
        json_object['end_ts'] = int(recording_timestampe_end)
        json_object['start_ts'] = int(recording_timestampe_start)

        json_object_final = {}
        json_object_final['data'] = json_object

        response = self.url_utils.get_request(url=device_detail_url, type=self.url_utils.TYPE_POST,
                                              input_json=json_object_final)
        event_list_meta_json = Url.parse(response.content.decode('utf8'))
        return event_list_meta_json

    def __get_mydlink_cloud_recordings_file(self, datas: json):
        list_initiate_url = "https://{openapi}/me/nvr/list/initiate?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )

        recordings_file = []
        counter = 1
        for data in datas:
            json_object = {}
            json_object['favorite'] = False
            json_object['timestamp'] = data['timestamp']
            json_object['subs_uid'] = data['act'][0]['subs_uid']
            json_object['mydlink_id'] = data['mydlink_id']

            json_object_final = {}
            json_object_final['data'] = json_object
            print("Request " + str(counter) + " von " + str(len(datas)))
            response_list_initiate = self.url_utils.get_request(url=list_initiate_url, type=self.url_utils.TYPE_POST,
                                                                input_json=json_object_final)

            response_list_initiate_json = Url.parse(response_list_initiate.content.decode('utf8'))

            cloud_video_url = "https://{openapi}/me/nvr/list/video.m3u8?session={session}&model=1".format(
                openapi=self.login_params.get('api_site')[0],
                session=response_list_initiate_json['data']['session_id']
            )

            response = self.url_utils.get_request(url=cloud_video_url, type=self.url_utils.TYPE_GET)
            recordings_file.append(response)
        return recordings_file
