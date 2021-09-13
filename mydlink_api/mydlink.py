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

    def __init__(self, email: str, password: str, proxy=None, disable_unverified_https_warn: bool = True):
        self.name = "PythonApi"
        self.email = email
        self.password = Hashing.md5Hashing(password)
        self.url_utils = Url(proxy=proxy, disable_unverified_https_warn=disable_unverified_https_warn)
        self.__login()

    def __login(self):
        oauth_sub_url = "/oauth/authorize2"
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

        response = self.url_utils.get_request(request_url, request_type=self.url_utils.TYPE_GET)
        self.login_params = Url.get_params(response)

    def get_device_list(self) -> json:
        device_list_url = "https://{openapi}/me/device/list?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )
        response = self.url_utils.get_request(url=device_list_url, request_type=self.url_utils.TYPE_GET)
        device_list_json = Url.parse(response.content.decode('utf8'))
        return device_list_json['data']

    def get_device_details(self, mydlink_id: str, mac: str) -> json:
        device_detail_url = "https://{openapi}/me/device/info?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )
        json_object = {'mac': mac, 'mydlink_id': mydlink_id}
        json_object_list = [json_object]
        json_object_final = {'data': json_object_list}

        response = self.url_utils.get_request(url=device_detail_url, request_type=self.url_utils.TYPE_POST,
                                              input_json=json_object_final)

        device_detail_json = Url.parse(response.content.decode('utf8'))
        return device_detail_json['data'][0]

    def get_mydlink_cloud_recordings_urls(self, year: int, month: int, day: int) -> []:
        event_list_meta_json = self.get_event_list_meta_infos(year, month, day)
        if 'path' in event_list_meta_json['data'][0]:
            response_all_events_details = self.url_utils.get_request(url=event_list_meta_json['data'][0]['path'],
                                                                     request_type=self.url_utils.TYPE_GET)
            all_events_details_json = Url.parse(response_all_events_details.content.decode('utf8'))
            all_events_details_json = all_events_details_json['data'][0]['data']
        else:
            all_events_details_json = event_list_meta_json['data'][0]['data']
        return self.__get_mydlink_cloud_recordings_file(all_events_details_json)

    def get_event_list_meta_infos(self, year: int, month: int, day: int) -> json:
        device_detail_url = "https://{openapi}/me/nvr/event/list?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )

        recording_date_start = datetime.datetime(year, month, day, 2, 00, 00)
        recording_date_end = datetime.datetime(year, month, day, 23, 59, 59, 999999)

        recording_timestampe_start = str(recording_date_start.timestamp()).replace(".", "") + "00"
        recording_timestampe_end = str(recording_date_end.timestamp()).replace(".", "")[0:13]

        json_object = {'end_ts': int(recording_timestampe_end), 'start_ts': int(recording_timestampe_start)}
        json_object_final = {'data': json_object}

        response = self.url_utils.get_request(url=device_detail_url, request_type=self.url_utils.TYPE_POST,
                                              input_json=json_object_final)
        event_list_meta_json = Url.parse(response.content.decode('utf8'))
        return event_list_meta_json

    def __get_mydlink_cloud_recordings_file(self, datas: json) -> []:
        list_initiate_url = "https://{openapi}/me/nvr/list/initiate?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )

        data = datas[0]
        json_object = {'favorite': False, 'timestamp': data['timestamp'], 'subs_uid': data['act'][0]['subs_uid'],
                       'mydlink_id': data['mydlink_id']}

        json_object_final = {'data': json_object}
        response_list_initiate = self.url_utils.get_request(url=list_initiate_url,
                                                            request_type=self.url_utils.TYPE_POST,
                                                            input_json=json_object_final)

        response_list_initiate_json = Url.parse(response_list_initiate.content.decode('utf8'))

        cloud_video_url = "https://{openapi}/me/nvr/list/video.m3u8?session={session}&model=1".format(
            openapi=self.login_params.get('api_site')[0],
            session=response_list_initiate_json['data']['session_id']
        )
        aws_recording_data = self.url_utils.stream_file(cloud_video_url).decode("utf-8").splitlines()

        def check_list(aws_recording_data):
            if 'https' in aws_recording_data:
                return True
            return False

        return list(filter(check_list, aws_recording_data))

    def get_mydlink_cloud_img_url(self, mydlink_id: str, event_timestamp: int) -> str:
        imagepath = None

        json_object = {'mydlink_id': mydlink_id, 'timestamp': event_timestamp}
        json_object_final = {'data': json_object}

        storyboard_img_url = "https://{openapi}/me/nvr/storyboard/info?access_token={access_token}".format(
            openapi=self.login_params.get('api_site')[0],
            access_token=self.login_params.get('access_token')[0]
        )

        response = self.url_utils.get_request(url=storyboard_img_url, request_type=self.url_utils.TYPE_POST,
                                              input_json=json_object_final)

        if response.status_code == self.url_utils.STATUS_CODE_SUCCESS:
            response_content = Url.parse(response.content.decode('utf8'))
            imagepath = response_content['data']['list'][0]['path']

        return imagepath
