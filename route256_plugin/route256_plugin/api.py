import requests


class DeviceApiHTTP:

    def __init__(self):
        self.host = 'http://localhost:8080'
        self.session = requests.Session()
        self.session.headers.update({"Authorization": 'Basic b3pvbjpyb3V0ZTI1Ng=='})

    def get_devices(self):
        response = self.session.get(f"{self.host}/api/v1/devices")
        return response.status_code
