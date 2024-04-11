import requests
from framework.rest.models import DeviceResponse


class DeviceAPI:
    def __init__(self, host, token):
        self.host = host
        self.session = requests.Session()
        self.session.headers.update({'Authorization': token})

    def get_device(self, device_id):
        url = f'{self.host}/api/v1/devices/{device_id}'
        response = self.session.get(url)
        assert response.status_code == 200, 'Wrong code'
        device_data = response.json().get('value') if response.ok else None
        return response.status_code, DeviceResponse(**device_data)

    def create_device(self, platform, user_id):
        url = f'{self.host}/api/v1/devices'
        data = {
            "platform": platform,
            "userId": user_id,
        }
        response = self.session.post(url, json=data)
        device_id = response.json().get('deviceId') if response.ok else None
        return response.status_code, device_id

    def delete_device(self, device_id: str):
        url = f'{self.host}/api/v1/devices/{device_id}'
        response = self.session.delete(url)
        device_data = response.json() if response.ok else None
        return response.status_code, device_data
