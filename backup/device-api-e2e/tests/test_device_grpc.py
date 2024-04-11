import pytest
from grpc import RpcError
from hamcrest import assert_that, equal_to

from data.device import PLATFORM, USER_ID, NONEXISTENT_DEVICE_ID


def test_get_device_grpc(device_api_grpc, device):
    device_data = device_api_grpc.get_device(int(device))

    assert_that(
        device_data.value.platform, equal_to(PLATFORM),
        f'Platform is {device_data.value.platform}',
    )
    assert_that(
        str(device_data.value.user_id), equal_to(USER_ID),
        f'UserID is {device_data.value.user_id}'
    )


def test_get_nonexistent_device_grpc(device_api_grpc):
    with pytest.raises(RpcError):
        device_api_grpc.get_device(NONEXISTENT_DEVICE_ID)
