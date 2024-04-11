## Запуск тестов
* Перейти в корень проекта
* Открыть консоль
* Выполнить команду `pytest`
* После запуска в корне проекта создастся папка allure-result

## Сгенерировать репорт
* Запустить команду `allure generate allure_result/ -c`
* Запустить команду `allure open` - в браузере откроется страница репорта

## Используемые библиотеки
* pytest
* allure
* requests
* logging
* re

## Test Suite: Тестирование endpoint`а /headers
Test Case | Шаги | Ожидаемый результат
------------ | ------------ | -------------
test_headers_content_type_equal_custom_content_type| Отправляем запрос на адресс http://httpbin.org/headers с заголовком content-type=custom_content_type | В теле ответа будет содержаться заголовок content-type=custom_content_type


## Test Suite: Тестирование endpoint`а /redirect/:n
Test Case | Шаги | Ожидаемый результат
------------ | ------------ | -------------
test_redirect_status| 1. Отправляем запрос http://httpbin.org/redirect/10 | каждый редирект содержит код состояния 302
test_count_of_redirect | 1. Отправляем запрос http://httpbin.org/redirect/10 |  выполненное количество редиректов равно запрашиваемому количеству
test_redirect_correct_location_url | 1. Отправляем запрос http://httpbin.org/redirect/10 | каждый редирект перенаправляет запрос на адрес http://httpbin.org/redirect/:n-1
test_last_redirect_must_be_get | 1. Отправляем запрос http://httpbin.org/redirect/1 | Location будет равен /get
test_by_default_redirect_is_relative | 1. Отправляем запрос http://httpbin.org/redirect/2 | Location будет равен /relative-redirect/1
test_relative_redirect | 1. Отправляем запрос http://httpbin.org/redirect/2?relative=true | Location будет равен /relative-redirect/1
test_absolute_redirect | 1. Отправляем запрос http://httpbin.org/redirect/2?absolute=true | Location будет равен http://httpbin.org/absolute-redirect/1
test_absolute_redirect_n_equal_1 | 1. Отправляем запрос http://httpbin.org/redirect/1?absolute=true | Location будет равен http://httpbin.org/get


## Test Suite: Тестирование endpoint`а /redirect/:n
>Каждый тест кейс тестировать со всеми типами запросов - 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'TRACE'

Test Case | Шаги | Ожидаемый результат
------------ | ------------ | -------------
test_status_valid_code | 1. Отправляем запрос с валидным статусом http://httpbin.org/status/406 | ответ содержит код состояния - 406
test_status_with_invalid_code | 1. Отправляем запрос с невалидным статусом http://httpbin.org/status/3-1 | ответ содержит код ошибки - 400
test_status_list_of_codes | 1. Отправляем запрос со списком кодов состояния http://httpbin.org/status/401,402,202 | ответ содержит один из кодов состояния - 401,402,202
test_status_list_of_codes_with_weight | 1. Отправляем запрос со списком кодов состояния и с указанием веса для каждого из них http://httpbin.org/status/401:2,402:1,202:4 | ответ содержит один из кодов состояния - 401,402,202
test_status_list_of_codes_with_negative_weight | 1. Отправляем запрос со списком кодов состояния и с указанием невалидного веса http://httpbin.org/status/401:-2,300:1 | ответ содержит код ошибки - 400
test_status_list_of_codes_with_invalid_weight | 1. Отправляем запрос со списком кодов состояния и с указанием невалидного веса http://httpbin.org/status/401:asd,300:1 | ответ содержит код ошибки - 400
test_status_one_code_with_weight | 1. Отправляем запрос с кодом состояния с указанием веса http://httpbin.org/status/401:2 | ответ содержит код ошибки - 400
test_status_list_of_codes_with_invalid_code | 1. Отправляем запрос с кодом состояния с указанием веса http://httpbin.org/status/401,402,200,foo | ответ содержит код ошибки - 400



> P.S.: Для теста `test_status_list_of_codes_with_negative_weight` на самом деле  возвращается ошибка - 500 (Внутрення ошибка сервера).Покопавшись в исходном коде httpbin, выяснил что действительно в сервере вылетает ислючение IndexError.Судя по коду я решил что более целесообразным было бы выбрасывать ошибку 400 и не поддерживать отрицательные веса.



