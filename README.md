# MyDlink-API-Python

Unofficial MyDlink API to give you access to Mydlink Cloud Devices example: D-Link DCS-8000LH or any D-Link Device witch use the MyDlinkAPP.


## Quickstart
 * **[Installation](#installation)**
 * **[Example-Code](#example-code)**

## Installation

Install using setup.py to pull all Python dependencies, or pip:

```
pip install git+https://github.com/ageof/MyDlink-API-Python.git
```
## Methoden
All Methode Return Json Objects
### get_device_list 
```json
      {
         "mac":"<DEVICE-MAC>",
         "mydlink_id":"<your_dlink_id>",
         "device_model":"<device-model>",
         "device_name":"<device-name>",
         "hw_ver":"<frimware version>",
         "online":>´<devices- online state>,
         "gen":<generation>,
         "hw_features":[

         ]
      }

```

 


## Example-Code
```python
import argparse
import mydlink_api


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="API to Connect MyDlink Cloud Devices")
    parser.add_argument('-e', '--email', dest='email', help='MyDlink email example maxmuster@muster.com')
    parser.add_argument('-p', '--password', dest='password', help='MyDlink password example Start123')
    parser.add_argument('-pr', '--proxy', dest='proxy', help='Porxy Url with or without credational')
    args = parser.parse_args()

    mydlink = mydlink_api.MyDlink(password=args.password, email=args.email, proxy=args.proxy)
    
    device_list_json = mydlink.get_device_list()
    device_info_json = mydlink.get_device_details(mac=device_list_json['mac'],
                                                  mydlink_id=device_list_json['mydlink_id'])

    mydlink.get_mydlink_cloud_recordings(year=2019, month=10, day=9)
```

# License:
MyDlink-API-Python is licensed under the GPLv3+: http://www.gnu.org/licenses/gpl-3.0.html.
