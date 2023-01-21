from hamcrest import assert_that, equal_to
from requests import codes

from data.device import PLATFORM, USER_ID


def test_get_device(device_api, device):
    status_code, device_data = device_api.get_device(device)

    assert_that(status_code, equal_to(codes.OK))
    assert_that(
        device_data.platform, equal_to(PLATFORM),
        f'Platform is {device_data.platform}',
    )
    assert_that(device_data.userId, equal_to(USER_ID))
