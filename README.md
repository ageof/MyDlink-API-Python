# MyDlink-Cloud-API-Python


Unofficial MyDlink API to give you access to Mydlink Cloud Devices example: D-Link DCS-8000LH or any D-Link Device witch use the MyDlinkAPP.


## Quickstart
 * **[Installation](#installation)**
 * **[Example-Code](#example-code)**
 * **[Methoden](#methoden)**

## Installation

Install using setup.py to pull all Python dependencies, or pip:

```
pip install git+https://github.com/ageof/MyDlink-API-Python.git
```
## Methoden
All Methode Return Json Objects
### get_device_list
Array of your Cloud Devices
```json
      {
         "mac":"<DEVICE-MAC>",
         "mydlink_id":"<your_dlink_id>",
         "device_model":"<device-model>",
         "device_name":"<device-name>",
         "hw_ver":"<frimware version>",
         "online": "<devices- online state as boolean>",
         "gen":"<generation as int>",
         "hw_features":[ ]
      }

```
### get_device_details
This function need the mydlink_id from get_device_list and mac from get_device_list.
The Return Json is a Detail List with all informaion about the selected Device.


```json
[
   {
      "mydlink_id":"",
      "device_model":"",
      "device_name":"",
      "verified":false,
      "password":"",
      "public_ip":"0.0.0.0",
      "public_port":"0",
      "private_ip":"192.XXX.XXX.XXX",
      "private_port":"8080",
      "auth_key":"XXXXXXXXXXXXX",
      "signal_addr":"mydlink_url",
      "online":true,
      "fw_uptodate":false,
      "fw_force":false,
      "fw_manual":false,
      "fw_ver":"2.01.XX",
      "agent_ver":"3.0.0-XX",
      "features":[
         2,
         9
      ],
      "ctrl_stats":"",
      "module_info":"",
      "utc_offset":0,
      "activate_date":"20XX-XX-XX XX:XX:XX.XX",
      "meta_info":"{\"photo_index\":\"\",\"room_type\":\"item_xxx_room\",\"Modules\":[]}",
      "units":[
         {
            "uid":0,
            "model":"",
            "setting":[
               21
            ],
            "status":[
               5,
               8
            ],
            "version":"2.01.XX"
         }
      ],
      "pin_code":"bluetooth pin",
      "lat":1,
      "promotion_info":{
         "level":0,
         "token":0
      },
      "olson_tz":"",
      "DCD":"wss:\/\/xxxx.mydlink.com:xxx\/SwitchCamera",
      "device_token":"xxxx",
      "da_url":"wss:\/\/192.XXX.XXX.XXX:8080\/SwitchCamera",
      "login_time":"",
      "local_liveview":"http:\/\/192.XXX.XXX.XXX:8088\/live.m3u8",
      "fw_latest":"2.02.XX",
      "agent_latest":"3.1.0-XX",
      "fw_latest_size":0
   }
]
```
### get_event_list_meta_infos
This function need a start and end timestamp like:
      recording_date_start = datetime.datetime(year, month, day, 2, 00, 00)
      recording_date_end = datetime.datetime(year, month, day, 23, 59, 59, 999999)
The Return Json is a List off all Cloud Events from your devices in this time range.
```json
      data:[
                  {
                  "start_ts":"timestmap as long",
                  "mydlink_no":"your_mydlink",
                  "path":"Amazon Web Services AWS URL"
                  },
            ]
      

```

#### get_mydlink_cloud_recordings
Dosen't work at the momement, coming sone 

### get_mydlink_cloud_img from event
This function need the timestamp and mydlink_id from the event, for this inforamtion use: get_event_list_meta_infos
mydlink_id=device_list_json[0]['mydlink_id']
event_timestamp=event['timestamp'])
The Return is a String with the url to the img witch is save in the aws from mydlink

## Example-Code
```python
import argparse

from mydlink_api.mydlink import MyDlink

if __name__ == "__main__":
      parser = argparse.ArgumentParser(
            description="API to Connect MyDlink Cloud Devices")
      parser.add_argument('-e', '--email', dest='email', help='MyDlink email example maxmuster@muster.com')
      parser.add_argument('-p', '--password', dest='password', help='MyDlink password example Start123')
      parser.add_argument('-pr', '--proxy', dest='proxy', help='Porxy Url with or without credational')
      args = parser.parse_args()

      mydlink = MyDlink(password=args.password, email=args.email, proxy=args.proxy)

      device_list_json = mydlink.get_device_list()
      device_info_json = mydlink.get_device_details(mac=device_list_json[0]['mac'],
                                                    mydlink_id=device_list_json[0]['mydlink_id'])

      date_list = [2021, 9, 8]
      events_list = mydlink.get_event_list_meta_infos(year=date_list[0], month=date_list[1], day=date_list[2])

      #This function dosent work at the moment, coming sone
      #mydlink.get_mydlink_cloud_recordings(year=date_list[0], month=date_list[1], day=date_list[2])

      cloud_img_list = []
      for event in events_list['data'][0]['data']:
            cloud_img_list.append(mydlink.get_mydlink_cloud_img(mydlink_id=device_list_json[0]['mydlink_id'],
                                                                event_timestamp=event['timestamp']))
```

# License:
MyDlink-API-Python is licensed under the GPLv3+: http://www.gnu.org/licenses/gpl-3.0.html.
