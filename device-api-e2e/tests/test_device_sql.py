from hamcrest import assert_that, equal_to
from framework.sql.ctx import entries_by_id


def test_get_device_sql(device_api_sql, device):
    new_device_id = int(device)

    entities = device_api_sql.entries_by_id(new_device_id)
    assert_that(len(entities), equal_to(1))


def test_get_device_sql_ctx(device):
    new_device_id = int(device)

    entities = entries_by_id(new_device_id)
    assert_that(len(entities), equal_to(1))


def test_get_device_sql_alchemy(device_api_orm, device):
    new_device_id = int(device)

    entities = device_api_orm.entries_by_id(new_device_id)
    assert_that(len(entities), equal_to(1))

    assert_that(entities[0].device_id, equal_to(new_device_id))
    assert_that(entities[0].payload['user_id'], equal_to(1))
