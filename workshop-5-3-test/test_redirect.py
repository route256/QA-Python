import re
import pytest
import allure
import requests
import logging

from helper import log_response


@allure.feature("Тестирование endpoint`а /redirect/:n")
@pytest.mark.skip('Skip.')
class TestRedirect:
    @allure.story("Код каждого редиректа равен 302")
    def test_redirect_status(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/10

        Ожидаемый результат: каждый редирект содержит код состояния 302
        """
        url = "http://httpbin.org/redirect/10"
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)
        assert response.history, "No one redirect did not happen"
        with allure.step("Проверяем, что код состояния для каждого url - 302"):
            for resp in response.history:
                logging.debug("Response code: %s for url %s" % (resp.status_code, resp.url))
                assert resp.status_code == 302, "Code not corresponds to redirect code - 302."

    @allure.story("Количество редиректов равно запрашиваемому количеству")
    def test_count_of_redirect(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/10

        Ожидаемый результат: выполненное количество редиректов равно запрашиваемому количеству
        """
        n = 10
        url = "http://httpbin.org/redirect/%s" % n
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)
        with allure.step("Проверяем, что количество выполненых редиректов равно %s" % n):
            assert len(response.history) == 10, "Length of redirects not corresponds expected length = %s" % n

    @allure.story("Location каждого url содержит :n = n-1")
    def test_redirect_correct_location_url(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/10

        Ожидаемый результат: каждый редирект перенаправляет запрос на адрес http://httpbin.org/redirect/:n-1
        """
        url = "http://httpbin.org/redirect/10"
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)

        assert response.history, "No one redirect did not happen"
        assert len(response.history) > 1, "Count of redirects must be higher than 1. Current count of redirects = %s" % len(response.history)
        logging.info("Request was redirected")
        with allure.step("Проверяем, что Location каждого url содержит :n = n-1"):
            for resp in response.history:
                location = resp.headers['Location']
                if location == '/get':
                    break
                location_redirect_id = re.match('.*redirect/(\d+)', location).group(1)
                resp_url_n = re.match('.*redirect/(\d+)', resp.url).group(1)
                assert int(location_redirect_id) == int(resp_url_n) - 1

    @allure.story("Последний редирект должен осуществляться на /get")
    def test_last_redirect_must_be_get(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/1

        Ожидаемый результат: Location будет равен /get
        """
        url = "http://httpbin.org/redirect/1"
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)
        assert response.history, "No one redirect did not happen"
        assert len(response.history) == 1, "Redirect should be only one. Current count of redirects = %s" % len(response.history)
        expected_location_url = '/get'
        with allure.step("Проверяем, что Location равен %s" % expected_location_url):
            location = response.history[0].headers['Location']
            assert location == expected_location_url, "Location must be equal '%s'. Current Location = %s" % (expected_location_url, location)

    @allure.story("По умолчанию, редиркет по относительному пути")
    def test_by_default_redirect_is_relative(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/2

        Ожидаемый результат: Location будет равен /relative-redirect/1
        """
        url = "http://httpbin.org/redirect/2"
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)
        assert response.history, "No one redirect did not happen"
        assert len(response.history) == 2, "Redirects should be two. Current count of redirects = %s" % len(response.history)
        expected_location_url = '/relative-redirect/1'
        with allure.step("Проверяем, что Location равен '%s'" % expected_location_url):
            location = response.history[0].headers['Location']
            assert location == expected_location_url, "Location must be equal '%s'. Current Location = %s" % (expected_location_url, location)

    @allure.story("Явное указание редиркета по относительному пути")
    def test_relative_redirect(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/2?relative=true

        Ожидаемый результат: Location будет равен /relative-redirect/1
        """
        url = "http://httpbin.org/redirect/2?relative=true"
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)
        assert response.history, "No one redirect did not happen"
        assert len(response.history) == 2, "Redirects should be two. Current count of redirects = %s" % len(response.history)
        expected_location_url = '/relative-redirect/1'
        with allure.step("Проверяем, что Location равен '%s'" % expected_location_url):
            location = response.history[0].headers['Location']
            assert location == expected_location_url, "Location must be equal '%s'. Current Location = %s" % (expected_location_url, location)

    @allure.story("Указание редиркета по абсолютному пути")
    def test_absolute_redirect(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/2?absolute=true

        Ожидаемый результат: Location будет равен http://httpbin.org/absolute-redirect/1
        """
        url = "http://httpbin.org/redirect/2?absolute=true"
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)
        assert response.history, "No one redirect did not happen"
        assert len(response.history) == 2, "Redirects should be two. Current count of redirects = %s" % len(response.history)
        expected_location_url = 'http://httpbin.org/absolute-redirect/1'
        with allure.step("Проверяем, что Location равен '%s'" % expected_location_url):
            location = response.history[0].headers['Location']
            assert location == expected_location_url, "Location must be equal '%s'. Current Location = %s" % (expected_location_url, location)

    @allure.story("Последний редирект по асболютному пути должен осуществляться на http://httpbin.org/get")
    def test_absolute_redirect_n_equal_1(self):
        """
        Шаги:
            1. Отправляем запрос http://httpbin.org/redirect/1?absolute=true

        Ожидаемый результат: Location будет равен http://httpbin.org/get
        """
        url = "http://httpbin.org/redirect/1?absolute=true"
        with allure.step("Отправляем запрос %s" % url):
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            log_response(response)
        assert response.history, "No one redirect did not happen"
        assert len(response.history) == 1, "Redirect should be only one. Current count of redirects = %s" % len(response.history)
        expected_location_url = 'http://httpbin.org/get'
        with allure.step("Проверяем, что Location равен '%s'" % expected_location_url):
            location = response.history[0].headers['Location']
            assert location == expected_location_url, "Location must be equal '%s'. Current Location = %s" % (expected_location_url, location)
