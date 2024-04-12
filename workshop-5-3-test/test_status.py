import allure
import pytest
import requests

from helper import log_response


@allure.feature("Тестирование endpoint`а /status/:code")
@pytest.mark.skip('Skip.')
class TestStatus:
    @pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'])
    @allure.story("Валидный код состояния")
    def test_status_valid_code(self, method):
        """
        Шаги:
            1. Отправляем запрос с валидным статусом http://httpbin.org/status/406

        Ожидаемый результат: ответ содержит код состояния - 406
        """
        with allure.step("Отправляем запрос %s на адрес 'http://httpbin.org/status/406'" % method):
            response = requests.request(method, 'http://httpbin.org/status/406', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что код состояния равен 406"):
            assert response.status_code == 406

    @allure.story("Невалидный код состояния")
    @pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'])
    def test_status_with_invalid_code(self, method):
        """
        Шаги:
            1. Отправляем запрос с невалидным статусом http://httpbin.org/status/3-1

        Ожидаемый результат: ответ содержит код ошибки - 400
        """
        with allure.step("Отправляем запрос %s на адрес 'http://httpbin.org/status/3-1'" % method):
            response = requests.request(method, 'http://httpbin.org/status/3-1', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что код состояния равен 400"):
            assert response.status_code == 400

    @allure.story("Список валидных кодов состояния")
    @pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'])
    def test_status_list_of_codes(self, method):
        """
        Шаги:
            1. Отправляем запрос со списком кодов состояния http://httpbin.org/status/401,402,202

        Ожидаемый результат: ответ содержит один из кодов состояния - 401,402,202
        """
        with allure.step("Отправляем запрос %s на адрес 'http://httpbin.org/status/401,402,202'" % method):
            response = requests.request(method, 'http://httpbin.org/status/401,402,202', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что вернулся один из кодов состояния 401,402,202"):
            assert response.status_code in (401, 402, 202)

    @allure.story("Список валидных кодов состояния с указанием веса для каждого кода")
    @pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'])
    def test_status_list_of_codes_with_weight(self, method):
        """
        Шаги:
            1. Отправляем запрос со списком кодов состояния и с указанием веса для каждого из них http://httpbin.org/status/401:2,402:1,202:4

        Ожидаемый результат: ответ содержит один из кодов состояния - 401,402,202
        """
        with allure.step("Отправляем запрос %s на адрес 'http://httpbin.org/status/401:2,402:1,202:4'" % method):
            response = requests.request(method, 'http://httpbin.org/status/401:2,402:1,202:4', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что вернулся один из кодов состояния 401,402,202"):
            assert response.status_code in (401, 402, 202)

    @allure.story("Список валидных кодов состояния с указанием одного отрицательно веса")
    def test_status_list_of_codes_with_negative_weight(self):
        """
        Шаги:
            1. Отправляем запрос со списком кодов состояния и с указанием невалидного веса http://httpbin.org/status/401:-2,300:1

        Ожидаемый результат: ответ содержит код ошибки - 400

        P.S.: На самом деле при указании отрицательного веса возвращается ошибка - 500 (Внутрення ошибка сервера).
              Покопавшись в исходном коде httpbin, выяснил что действительно в сервере вылетает ислючение IndexError.
              Судя по коду я решил что более целесообразным было бы выбрасывать ошибку 400 и не поддерживать отрицательные веса.
        """
        with allure.step("Отправляем запрос на адрес 'http://httpbin.org/status/401:-2,300:1'"):
            response = requests.get('http://httpbin.org/status/401:-2,300:1', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что вернулся код ошибки 400"):
            assert response.status_code == 400

    @allure.story("Список валидных кодов состояния с указанием одного невалидного веса")
    @pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'])
    def test_status_list_of_codes_with_invalid_weight(self, method):
        """
        Шаги:
            1. Отправляем запрос со списком кодов состояния и с указанием невалидного веса http://httpbin.org/status/401:asd,300:1

        Ожидаемый результат: ответ содержит код ошибки - 400
        """
        with allure.step("Отправляем запрос %s на адрес 'http://httpbin.org/status/401:asd,300:1'" % method):
            response = requests.request(method, 'http://httpbin.org/status/401:asd,300:1', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что вернулся код ошибки 400"):
            assert response.status_code == 400

    @allure.story("Один код состояния с указанием веса")
    @pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'])
    def test_status_one_code_with_weight(self, method):
        """
        Шаги:
            1. Отправляем запрос с кодом состояния с указанием веса http://httpbin.org/status/401:2

        Ожидаемый результат: ответ содержит код ошибки - 400
        """
        with allure.step("Отправляем запрос %s на адрес 'http://httpbin.org/status/401:2'" % method):
            response = requests.request(method, 'http://httpbin.org/status/401:2', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что вернулся код ошибки 400"):
            assert response.status_code == 400

    @allure.story("Список кодов состояния с одним невалидным кодом")
    @pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'])
    def test_status_list_of_codes_with_invalid_code(self, method):
        """
        Шаги:
            1. Отправляем запрос с кодом состояния с указанием веса http://httpbin.org/status/401,402,200,foo

        Ожидаемый результат: ответ содержит код ошибки - 400
        """
        with allure.step("Отправляем запрос %s на адрес 'http://httpbin.org/status/401,402,200,foo'" % method):
            response = requests.request(method, 'http://httpbin.org/status/401,402,200,foo', timeout=60)
            log_response(response)
        with allure.step("Проверяем, что вернулся код ошибки 400"):
            assert response.status_code == 400
