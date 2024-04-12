# Workshop 6  Performance-testing

Репозиторий для воркшопа по нагрузочному тестированию

Образы для предварительного скачивания:

````
docker pull grafana/grafana:latest
docker pull victoriametrics/victoria-metrics:latest
docker pull prom/node-exporter:latest
docker pull yandex/yandex-tank:latest
docker pull yandex/yandex-tank:jmeter-latest


````

make dc-up

docker network ls

docker ps - список всех запущенных контейнеров

docker container logs -f [container name] - аналог tail -f

## Часть 1 Мониторинг (40 мин)

Victoria Metrics (Prometheus)

1) Добавляем в **docker-compose.yaml** секцию с системой мониторинга victoria-metrics

   ```
   victoria:
     container_name: victoria-metrics
   	# - Используем образ victoria-metrics вместо обычного prometheus
     # - Потому что он может притворяться influxDB и TSDB - что очень удобно для НТ
     image: victoriametrics/victoria-metrics
     restart: unless-stopped
     # - Открываем порты виктории для HTTP метрик
     ports:
       - "8428:8428"
       - "4242:4242"
       - "8089:8089/tcp"
       - "8089:8089/udp"
     volumes:
   	# - Локальная директория для мониторинга
       - ./docker/victoria:/victoria-metrics-data
   	# - Подключаем файл с конфигурацией прометеуса -именно в нем мы будем настраивать таргеты
       - ./prometheus.yml:/prometheus.yml
     command:
   	# - Включаем opentsdb
       - -opentsdbHTTPListenAddr=:4242
   	# - Включаем influx
       - -influxListenAddr=:8089
   	# - Подключаем Прометеус конфиг файл
       - -promscrape.config=/prometheus.yml
   	# - Подключаем к сети наших контейнеров
     networks:
       - ompnw
   ```
2) Заменяем содержимое файла **prometheus.yml** в корне проекта на следующее:

```
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: 'victoria'
    static_configs:
      - targets:
        - localhost:8428
```

3) Выполняем команду **make dc-up**
4) Корень victoria-metrics доступен по адресу: http://localhost:8428/

---

### Grafana

1) Добавляем секцию Grafana Docker в файл **docker-compose.yaml**

```
grafana:
  image: grafana/grafana:latest
  container_name: grafana
  ports:
    - "3000:3000"
  volumes:
    - ./docker/grafana/provisioning:/etc/grafana/provisioning/
    - ./docker/grafana/data:/var/lib/grafana/
  environment:
    GF_SECURITY_ADMIN_USER: admin
    GF_SECURITY_ADMIN_PASSWORD: admin
    GF_INSTALL_PLUGINS: "grafana-clock-panel,briangann-gauge-panel,natel-plotly-panel,grafana-simple-json-datasource"
    GF_AUTH_ANONYMOUS_ENABLED: "true"
  networks:
    - ompnw
```

2) Выполняем команду ```make dc-up``` чтобы скачать и запустить Grafana.
3) Заходим в Grafana на [http://localhost:3000](http://localhost:3000)  и логинимся  ```Login: admin Password: admin```
4) Настраиваем источник данных: **Configuration→ Data Sources->Add DataSource**
5) Выбираем тип **DataSource -> Prometheus** - Так как VictoriaMetrics - полностью имплементит Prometheus API
6) Заполняем источник данных:

   1) Имя оставляем как есть - **Prometheus**
   2) Указываем адрес: http://victoria-metrics:8428 - данные тянутся через back-end - так что необходимо указать доменное имя внутри docker-network
   3) Жмем кнопку: SaveAndTest - Должен появится зеленый квадратик.
7) Теперь надо настроить первый Dashboard - традиционно - это Dashboard системы мониторинга.

   1) Жмем на 4 квадратика и выбираем import
   2) Вводим в поле **Import via grafana.com**: 10229 [Grafana-Dashboard for VictoriaMetrics](https://grafana.com/grafana/dashboards/10229-victoriametrics/)
   3) Жмем Load
   4) Оказываемся на Dashboard - с метриками Victoria-Metrics

   ---

   Node Exporter
8) Настраиваем Экспортер метрик с вашей машины: node-exporter

   1) Добавляем еще 1 контейнер в наш docker-compose.yaml

```
node-exporter:
  image: prom/node-exporter:latest
  container_name: node-exporter
  restart: unless-stopped
  expose:
    - 9100
  networks:
    - ompnw
```

2) Выполняем make **dc-up**
3) Подключаем мониторинг к этому экспортеру:
   В файл prometheus.yml добавляем новую Джобу:

```
- job_name: node_exporter
  static_configs:
    - targets: [node-exporter:9100]
```

4) Выполняем: [http://localhost:8428/-/reload](http://localhost:8428/-/reload) - Заставляем Victoria-Metrics перечитать конфиги
   1) Для удобства - добавляем в Makefile следующие секции

```
.PHONY: prom-refresh
prom-refresh:
	curl 'http://localhost:8428/-/reload'

.PHONY: prom-config
prom-config:
	curl 'http://localhost:8428/config'

.PHONY: prom-status
prom-status:
	 curl 'http://localhost:8428/api/v1/targets'|jq '.data.activeTargets| .[] | {pool:.scrapePool, status:.health}'
```

5) Выполняем ```make prom-refresh``` - Перезагружаем конфиги экспортеров
6) Удостоверяемся что они распарсились: ```make prom-config```
7) Заходим в Grafana и добавляем Дашборд для node_exporter: **1860** и сохраняем его.

---

### Добавляем мониторинг act-device-api

1) Добавляем новую секцию **prometheus.yml**

```
  - job_name: device-api
    static_configs:
      - targets: [ act-device-api:9100 ]
```

2) **make prom-refresh & make prom-config**
3) Смотрим что за метрики экспортируются: Заходим в http://localhost:8428/targets - Нажимаем на responce - соответствующего экспортера
4) Смотрим на метрики

---

### Создаем свой Дашбоард

1) Открываем  Grafana http://localhost:3000
2) 4 квадрата-> New Dashboard
3) Надо создать несколько переменных для выпадающих боксов: **Settings->Variables->Add Variable**
4) Нам нужно создать список всех инстансов сборки статистики - Для этого используем функцию в поле query:```label_values(up{job='device-api'},instance) ```[Подробнее про доступные функции](https://grafana.com/docs/grafana/latest/datasources/prometheus/#query-variable)
5) Появляется список из 1 элемента. Это нормально.
6) Сохраняем переменную и выходим из настроен борды. Сохраняем ее.
7) Создаем Dashboard для мониторинга вашего приложения:
   1) Кликаем на Add new Panel
   2) Переходим в настройку панели и добавляем метрику: grpc_server_handled_total в поле query

```
sum(rate(grpc_server_handled_total{instance=~'$instance'}[1m])) by (grpc_method)
```

8) Настраиваем название панели и остальные настройки по желанию.
9) Нажимаем кнопку Apply
10) Сохраняем борду

---

## Осваиваем Yandex-Tank + Pandora (40 мин)

## Предварительные условия

Давайте вначале запустим наш проект. (Система мониторинга должна быть уже настроена):

1) Скачаем базовый Docker образ для этого Воркшопа.

```docker pull yandex/yandex-tank:latest```

2) Перейдем в act-device-api проект и создадим папку loadtests.
3) Перейдем в папку loadtests **(cd loadtests)**
4) Создадим там файл load.yaml (touch load.yaml)
5) Добавим в него следующее содержимое:

```yaml
phantom:
  enabled: false # - Phantom плагин - надо отключить - так как он включен по умолчанию
pandora:
  enabled: true # - Pandora - плагин - надо включить 
  package: yandextank.plugins.Pandora 
  pandora_cmd: /usr/local/bin/pandora # Адрес бинарника пандоры - Когда сделаете свою пушку - тут поменяйте на свой
  config_content: # - содержиме этой секции надо настриавать по исходникам Pandora - в зависимости от Типа используемой пушк и патронов. (Содержимое этой секции - это содержимое файла с конфигом пандоры.;
    pools: # - Пуллов потоков может быть много в рамках одной пандоры.
      - id: HTTP pool 
        ammo:
          type: http/json
          file: device-api-jsonline.ammo
        gun:
          target: act-device-api:8080
          type: http
          ssl: false
          dial:
            timeout: 2s
        rps:
          - duration: 1m30s
            from: 1
            to: 50
            type: line
          - type: const
            duration: 2m
            ops: 50
        startup:
          type: once
          times: 50 # - количество выделенных горутин для теста. На запрос-ответ - в 1 момент времени - расходуется 1 горутина. Формула для вычисления необходимых горутин: RPS * <max response time in Milliseconds> / 1000 Для примера - максимальное время отклика вашего сервиса - 2.5 секунды и целевой РПС - 1230, вам необходимо будет: 1230 * 2500 / 1000 = 3075 Горутин..
console:
  enabled: true # Включим вывод Информации в консоль.
telegraf:
  enabled: false
```

6) Создадим файл **device-api-jsonline.ammo** - это формат патронов в **jsonline** формате (кодируем запрос в виде JSON)
7) Поместим в него следующую строку

```
{"tag":"req1", "uri": "/api/v1/devices?page=1&perPage=100", "method": "GET", "headers": {"Accept": "application/json"},"body": "", "host": "act-device-api"}
```

9) Документация по секциям Yandex-tank: https://yandextank.readthedocs.io/en/latest/config_reference.html
10) Давайте посмотрим - как называются ваши docker сети:
    ```docker network ls```
    В Выводе будет нечто вроде:

```
NETWORK ID     NAME                  DRIVER    SCOPE
656d0a4bd3ad   bridge                bridge    local
60dfcdd27f4b   host                  host      local
31029ec934e2   none                  null      local
dc70c0ec7132   ozon_route256_ompnw   bridge    local
```

Вам нужна сеть с названием: route256...
9) Запустим наш тест:

```bash
cd ./loadtest
docker run --network ozon_route256_ompnw -v $(pwd):/var/loadtest --rm -it yandex/yandex-tank:latest -f load.yaml
```

Давайте разберем еще раз эту команду:

- --network - Запускает наш контейнер в docker сети, в которой запущен наш основной проект.
- -v $(pwd):/var/loadtest - Мы подключаем текущую папку - внутрь контейнера по пути: /var/loadtest
- --rm - Удаляем старые контейнеры (если не сделать - будем падать - что такой контейнер уже есть)
- -it - Сокращение инструкций --interactive и --tty  - которые позволяют работать с docker-котейнерами как с утилитами командной строки.

В результате у вас в папке loadtests повится папка logs в которой по датам - будут лежать артефакты вашего запуска:

* validated_conf.yaml - Итоговый файл с конфигом, после всех преобразований. В yandex-tank есть механизм оверрайда конфигов. Можно построить свои конфиги на основе шаблонов, которые будут оверрайдится итоговым файлом. В нашем случае - мы оверрайдим дефолтную конфигурацию. Полная итоговая конфигурация - расположена в данном файле.
* tank.log - Логи самого yandex-tank - Бывает полезно сюда заглянуть.
* pandora_****.log - Логи Pandora генератора. Про конфиги пандоры - Яндекс-танк ничего не знает. Поэтому и проверить их не может. Если тест запускается и сразу стопается - смотреть надо именно сюда. Скорее всего - где-то ошибка в конфигах пандоры.
* pandora_config_****.yaml - Итоговый конфиш пандоры, который собрал Yandex-tank из итогового файла с конфигом.

9) Настроим запись статистики теста в Victoria-metrics
   1) Добавим в секцию с конфигом: следующий блок:

```yaml
opentsdbuploader:
  enabled: true
  package: yandextank.plugins.OpenTSDBUploader
  tank_tag: "local" # - Можем добавить к танку дополнительный тег
  address: victoria-metrics
  port: 4242
  username: ""
  password: ""
  ssl: false
  histograms: true
  verify_ssl: false
  labeled: true
  custom_tags:
```

2) Зайдем в Grafana http://localhost:3000/ и не забываем залогиниться.
3) В репозитории с воркшопом скопируем содержимое файла: Yandex-tank-dashboard.json
4) В Grafana 4 квадрата ->Import-> Вставить содержимое в поле: `Import via panel json` и нажать кнопку import.
5) Разбираемся в борде.
6) Дальнейшие шаги - Придумывать тесты. Разбираться с форматами пушек и патронов. (Код - лучшая документация!)



### Стрельбы по grpc

1) Перейдем в act-device-api проект и создадим папку loadtests.
2) Перейдем в папку loadtests **(cd loadtests)**
3) Создадим там файл load.yaml (touch load.yaml)
4) Добавим в него следующее содержимое:

```yaml
phantom:
  enabled: false # - Phantom плагин - надо отключить - так как он включен по умолчанию
pandora:
  enabled: true # - Pandora - плагин - надо включить
  package: yandextank.plugins.Pandora
  pandora_cmd: /usr/local/bin/pandora # Адрес бинарника пандоры - Когда сделаете свою пушку - тут поменяйте на свой
  config_content: # - содержиме этой секции надо настриавать по исходникам Pandora - в зависимости от Типа используемой пушк и патронов. (Содержимое этой секции - это содержимое файла с конфигом пандоры.;
    pools: # - Пуллов потоков может быть много в рамках одной пандоры.
      - id: Grpc pool
        ammo:
          type: grpc/json
          file: grpc.ammo
        gun:
          target: act-device-api:8082
          type: grpc
          tls: false
        rps:
          - duration: 1m30s
            from: 1
            to: 100
            type: line
          - type: const
            duration: 2m
            ops: 100
        startup:
          type: once
          times: 250 # - количество выделенных горутин для теста. На запрос-ответ - в 1 момент времени - расходуется 1 горутина. Формула для вычисления необходимых горутин: RPS * <max response time in Milliseconds> / 1000 Для примера - максимальное время отклика вашего сервиса - 2.5 секунды и целевой РПС - 1230, вам необходимо будет: 1230 * 2500 / 1000 = 3075 Горутин..
console:
  enabled: true # Включим вывод Информации в консоль.
telegraf:
  enabled: false
opentsdbuploader:
  enabled: true
  package: yandextank.plugins.OpenTSDBUploader
  tank_tag: "local" # - Можем добавить к танку дополнительный тег
  address: victoria-metrics
  port: 4242
  username: ""
  password: ""
  ssl: false
  histograms: true
  verify_ssl: false
  labeled: true
  custom_tags:
```

5) Создадим там же файл grpc.ammo со следующим содержимым:
```
{"tag": "CreateDeviceV1", "call": "ozonmp.act_device_api.v1.ActDeviceApiService.CreateDeviceV1", "payload": {"platform": "ios", "user_id": 1}}
```
6) Запустим тест, выполнив команду: 

```bash
docker run --network ozon_route256_ompnw -v $(pwd):/var/loadtest --rm -it yandex/yandex-tank:latest -c load-grpc.yaml
```

7) Идем на дашбоард и наблюдаем за метркиами


### Дополнительные ссылки:

https://habr.com/ru/company/southbridge/blog/455290/
https://habr.com/ru/company/timeweb/blog/562378/
https://habr.com/ru/company/otus/blog/501978/


Про метрики go-grpc:
https://github.com/grpc-ecosystem/go-grpc-prometheus/blob/master/README.md

Пример мониторинга Посгреса:

postres-exorter

```yaml
postgres-exporter:
  container_name: postgres-exporter
  restart: always
  image: quay.io/prometheuscommunity/postgres-exporter
  networks:
    - ompnw
  environment:
    DATA_SOURCE_NAME: "postgresql://postgres:password@postgres:5432/postgres?sslmode=disable"
  ports:
    - "9187:9187"
```

```make dc-up```

Добавляем правило в prometheus.yml

```yaml
- job_name: postgres
  static_configs:
    - targets: [postgres-exporter:9187]
```

Выполняем:

```make prom-refresh```

Заходим в grafana и добавляем борду [https://grafana.com/grafana/dashboards/9628-postgresql-database/](https://grafana.com/grafana/dashboards/9628-postgresql-database/) ID: 9628
Проходимся по борде.
