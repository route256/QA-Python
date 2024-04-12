import pytest
import time
import requests
from route256_plugin.api import DeviceApiHTTP


@pytest.fixture(scope='session', autouse=True)
def wait_service():
    def _wait(count=1):
        try:
            status = DeviceApiHTTP().get_devices()
            while not status == 200:
                status = DeviceApiHTTP().get_devices()
                time.sleep(0.5)
                return _wait(count=count + 1)
        except requests.exceptions.ConnectionError:
            return _wait(count=count + 1)
        finally:
            if count == 15:
                return
    _wait()
