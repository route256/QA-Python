import allure
import requests

from helper import log_response


@allure.feature("Тестирование endpoint`а /headers")
class TestHeaders:
    @allure.story("Заголовок с  content-type=custom_content_type")
    def test_headers_content_type_equal_custom_content_type(self):
        """
        Шаги тест кейса:
            1. Отправляем запрос на адресс http://httpbin.org/headers с заголовком content-type=custom_content_type

        Ожидание:
            В теле ответа будет содержаться заголовок content-type=custom_content_type
        """
        with allure.step("Отправляем запрос на адресс http://httpbin.org/headers с заголовком content-type=custom_content_type"):
            response = requests.get("http://httpbin.org/headers", headers={"content-type": 'custom_content_type'}, timeout=30)
            log_response(response)
        with allure.step("Проверяем что в теле ответа содержится заголовок content-type=custom_content_type"):
            assert response.json()["headers"]["Content-Type"] == "custom_content_type", "Content-Type not corresponds to %s" % "custom_content_type"
