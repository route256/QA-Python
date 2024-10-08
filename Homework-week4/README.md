# Домашнее задание - тесты на логирование и отчёт о тестировании

## Дано:

Как всякий хороший клиентский сервис, device-api сохраняет логи CRUD-операций над девайсами.
На лекции мы посмотрели несколько примеров [тестовых DB клиентов](https://gitlab.ozon.dev/qa/classroom-5/students/device-api-e2e/-/tree/master/src/sql) для device-api. 
Нужно использовать любой из них для тестов логирования.

Помимо этого, если сейчас тест упадет, без чтения кода теста не разобраться, что нужно починить. Нужно сформировать allure-отчёт.


## Задание:
- Напишите набор автотестов для логирования CRUD-операций
- Добавьте в ваши существующие тесты логирование в отчёт allure

## Критерии приемки задания:
- тесты на SQL-логи в отдельном файле
- проверяются все CRUD-операции
- проверяется, что действие логируется один раз
- проверяется, что payload соответствует запросу
- есть негативные тесты
- после прогона тестов формируется отчёт
- отчёт есть в MR
- тесты на REST/gRPC/логи в отдельных suites
- если шаг есть в тесте - он есть в отчёте тоже
- если есть setup/teardown - они есть в отчёте тоже

## Задание со звёздочкой *
За каждый пункт начисляется бонусный балл.
- кодстайл соотвествует PEP8
- для проверки переиспользуется payload из реально выполненного запроса
- добавить информацию для дебага в allure-отчет: для REST к отчёту приложен файл с body и headers запросов и ответов, для gRPC - сообщения, сериализованные в json, для логов SQL - запрос в txt, и результат в json
