
- [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
- [kafka-ui](https://github.com/provectus/kafka-ui)
- [Параметры](https://kafka.apache.org/documentation/#consumerconfigs)
- [Консольная утилита](https://kafka.apache.org/quickstart)
- [Библиотека для ретрая](https://pypi.org/project/retrying/)

Команда для сдвига оффсета.
```shell
/kafka/bin/kafka-consumer-groups.sh --bootstrap-server 127.0.0.1:9092 --group route --reset-offsets --to-latest --topic order-events --execute
```

Команда для просмотра информации по консьюм группе.
```shell
/kafka/bin/kafka-consumer-groups.sh --describe --group route --bootstrap-server 127.0.0.1:9092
```