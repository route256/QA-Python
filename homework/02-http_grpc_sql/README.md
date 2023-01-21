# Домашнее задание - собрать коллекцию postman для вызовов device-api

## Дано:

На занятии мы поговорили про swagger нашего тестового сервиса. Поняли, что одного swagger для тестирования grpc нам недостаточно. И увидели, что в postman есть все инструменты для тестов и REST и gRPC.

## Задание:

- Соберите коллекцию postman для тестирования REST device-api
    - запросы должны содержать тестовые данные
    - должны проверяться [response codes](https://learning.postman.com/docs/writing-scripts/script-references/test-examples/#getting-started-with-tests)
    - должен успешно проходить запуск в newman

- Проверьте работу вызовов и reflection gRPC device-api


## Критерии приемки задания:

- бранч QAHW-2 и папка с решением в вашей копии device-api
- коллекция c REST из postman в коммите
- результат запуска в newman в тексте MR

## Подсказки:

Используйте импорт описания из swagger, чтобы сэкономить время. Postman [пока не поддерживает тесты и импорт коллекций gRPC](https://blog.postman.com/postman-now-supports-grpc/).

[Установка Postman](https://learning.postman.com/docs/getting-started/installation-and-updates/#contents).

[Установка Newman](https://learning.postman.com/docs/running-collections/using-newman-cli/command-line-integration-with-newman/).


# Домашнее задание со звездочкой - поиск в таблице devices_events

## Дано

В результате ошибки стажера на нескольких устройствах теперь установлен Freebsd. Нужно, используя SQL и записи в логах выяснить, какая OS была на них установлена до этого инцидента.

## Задание

Напишите SQL, который выводит предыдущие значения поля platform для устройств с `platform = 'Freebsd'`. Исторические данные хранятся в devices_events.


## Критерии приемки задания:

- бранч QAHW-2 и папка с решением в вашей копии device-api
- SQL код, который можно запустить в клиенте и который покажет желаемый результат в коммите
- его вывод с вашей версии DB (данные генерятся рандомно и отличаются на всех инстансах) в тексте MR 
