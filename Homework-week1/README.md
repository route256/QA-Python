# Домашнее задание - разделить учебный docker-compose.yml на два

## Дано:

На занятии мы описали в конфиге нужные act-device-api сервисы: базу данных postgres, ещё там есть nginx, swagger-ui и сервис для сохранения трейсов. Мы собрали и запустили приложение, и увидели, что оно проходит live-check.

Сейчас вся связка сервисов настроена у нас в одном docker-compose.yml. Так же есть ещё два конфига - для отдельного запуска только postgres & jaeger и нашего тестового сервиса с nginx и swagger-ui.

Зачем нужно отдельно запускать DB? Для целей разработки нам может понадобиться запустить наш сервис не внутри контейнера - а при помощи ```make run``` или из IDE. При этом у него должен быть доступ к postgres.


## Задание:

- Допишите в makefile команды 
    - команду для запуска связки сервисов из двух раздельных конфигов
    - команду для выключения связки сервисов из двух раздельных конфигов
    - команду для запуска отдельно только сервисов из docker-compose.service-env

- Проверьте, что все по-прежнему работает после запуска из раздельных конфигов - livecheck, ручки в swagger
- Проверьте, что можно запустить, выключить и снова запустить сервисы вашими make командами.


## Критерии приемки задания:

- изменения в Makefile в коммите
- вывод `docker compose ps` в описании MR после запуска сервисов

## Подсказки:

1976 год - создана утилита make. Даже сейчас она активно используется в разработке. С её помощью можно сохранять алиасы сложных команд вместе с кодом репозитория (хотя это и не совсем использование по-назначению, в первую очередь это инструмент сборки).

В качестве разделитей используются табы. Stuart Feldman утверждает, [что это обратная совместимость](http://catb.org/~esr/writings/taoup/html/ch15s04.html).

Синтаксис Makefile прост, вот шпаргалка по формату одного из существующих rule:

```
.PHONY: dc-build   <- нужно собирать всегда, потому что это не файл
dc-build: dc-down  <- название target, запускаем как make dc-build. Перед этой командой выполнится dc-down.
	docker-compose -p ozon_route256 up -d --no-deps --build --force-recreate act-device-api		# эту команду выполнит make
```

Посмотреть список сетей docker:
```bash
docker network ls
```

Посмотреть список образов docker:
```bash
docker images
```


## Как сдавать домашние задания
Наш курс построен так, чтобы мы научились работать с конкретным сервисом и покрывать его проверками.
Сервис лежит в репозитории. Его разрабатывали разработчики на курсе Go школы.
Наша задача - научиться этот сервис тестировать.
За весь курс ваш РЕПОЗИТОРИЙ должен будет обрасти всевозможными тестами, линтерами и пайплайнами.

## Как сделать себе РЕПОЗИТОРИЙ для сдачи домашних заданий?

- НУЖНО себе в приватную папку форкнуть репозиторий с сервисом. В гитлабе на странице проекта нажать `Fork`, выбрать namespace с вашим именем, выбрать `Visibility level = private`, нажать `Fork project`
- Порвать форк-связь. `Settings` > `Advanced` > `Remove fork relationship`
- Дать доступ в репозиторий тьюторам и преподавателям. `Project information` > `Members` > `Invite member`, пригласить своего тьютора с правами `Maintainer`
- Это будет ваш рабочий РЕПОЗИТОРИЙ, в котором НУЖНО будет выполнять домашние задания

## Как сдавать домашние задания?

- Домашние задание НУЖНО будет оформлять MR (merge-request) в СВОЕМ репозитории
- Тьюторы БУДУТ проверять MR и оставлять комментарии
- Если все хорошо, тьюторы дадут аппрув, и MR МОЖНО слить в РЕПОЗИТОРИЙ




