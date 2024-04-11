from flake8_plugin_utils import assert_error, assert_not_error

from flake8route.flake8route import (
    Flake8RouteAllureVisitor, MissingAllureIdError
)


def test_code_with_no_id():
    assert_error(
        Flake8RouteAllureVisitor,
        'def test_some():\n'
        '    pass',
        MissingAllureIdError,
    )


def test_code_with_id_tag():
    assert_not_error(
        Flake8RouteAllureVisitor,
        '@allure.id("1")\n'
        'def test_some():\n'
        '    pass',
    )
