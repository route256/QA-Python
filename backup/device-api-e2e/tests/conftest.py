import pytest

from framework.rest.api import DeviceAPI
from framework.grpc.api import DeviceAPIGRPC
from config import HOST_REST, HOST_GRPC, TOKEN, DSN
from data.device import PLATFORM, USER_ID
from framework.sql.alchemy import Alchemy
from framework.sql.client import SQLDeviceApi


@pytest.fixture(scope='session')
def device_api():
    return DeviceAPI(HOST_REST, TOKEN)


@pytest.fixture(scope='session')
def device_api_grpc():
    return DeviceAPIGRPC(HOST_GRPC)


@pytest.fixture(scope='function')
def device(device_api):
    _, device_id = device_api.create_device(platform=PLATFORM, user_id=USER_ID)

    yield int(device_id)

    device_api.delete_device(device_id)


@pytest.fixture(scope='function', params=['REST', 'GRPC'])
def client(request, device_api_grpc, device_api):
    if request.param == 'REST':
        return device_api
    elif request.param == 'GRPC':
        return device_api_grpc
    else:
        raise ValueError()


@pytest.fixture(scope='session')
def device_api_sql():
    return SQLDeviceApi(dsn=DSN)


@pytest.fixture(scope='session')
def device_api_orm():
    return Alchemy(dsn=DSN)
