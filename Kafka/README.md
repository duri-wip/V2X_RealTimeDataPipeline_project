## 개요
Apache Kafka는 분산 스트리밍 플랫폼으로, 실시간 데이터 파이프라인과 스트리밍 애플리케이션을 구축할 수 있게 해줍니다. Kafka의 높은 처리량, 내결함성, 확장성은 데이터 파이프라인의 필수 구성 요소입니다.

## 아키텍처
우리의 데이터 파이프라인 아키텍처에서 Kafka의 역할은 다음과 같습니다:
1. **데이터 수집**: Kafka는 다양한 소스로부터 실시간 데이터를 수집하여 여러 토픽으로 전송합니다.
2. **처리**: Apache Spark가 Kafka 토픽의 데이터를 처리합니다.
3. **저장**: 처리된 데이터는 Hadoop과 PostgreSQL에 저장되어 추가 분석에 사용됩니다.
4. **시각화**: Jupyter Lab을 사용하여 데이터를 시각화합니다.

## 설치 및 설정
Kafka를 시작하려면 다음 단계를 따르세요:

### 사전 요구사항
- Java 8 이상
- ZooKeeper (Kafka는 ZooKeeper를 필요로 합니다)

### 설치
1. **Kafka 다운로드**:
    ```bash
    wget https://downloads.apache.org/kafka/3.5.2/kafka_2.13-3.5.2.tgz
    tar -xzf kafka_2.13-3.5.2.tgz
    cd kafka_2.13-3.5.2
    ```

2. **ZooKeeper 시작**:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    ```

3. **Kafka 브로커 시작**:
    ```bash
    bin/kafka-server-start.sh config/server.properties
    ```

## 구성
Kafka 설정은 `config/server.properties` 파일을 편집하여 사용자 정의할 수 있습니다. 주요 설정은 다음과 같습니다:

- **브로커 ID**:
    ```properties
    broker.id=0
    ```

- **로그 디렉터리**:
    ```properties
    log.dirs=/app/kafka-logs
    ```

- **ZooKeeper 연결**:
    ```properties
    zookeeper.connect=server01:2181,server02:2181,server03:2181
    ```

## 사용법
### 토픽 생성
`my-topic`이라는 Kafka 토픽을 생성하려면:
```bash
bin/kafka-topics.sh --create --topic my-topic --bootstrap-server server01:9092,server02:9092,server03:9092 --replication-factor 1 --partitions 1
```
## Kafka Producer
Kafka Producer는 Apache Kafka로 데이터를 전송하는 역할을 합니다. 

이 프로듀서는 Kafka 클러스터의 브로커에 메시지를 보내어 특정 토픽에 데이터를 게시합니다. 

코드 내에서 KafkaProducer 클래스는 다음과 같은 방식으로 사용됩니다:

### 코드 설명
- KafkaProducer 객체 생성:

```python
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
```
bootstrap_servers: Kafka 브로커의 주소를 지정합니다.

value_serializer: 데이터를 JSON 형식으로 직렬화하여 바이트로 인코딩합니다.

- 데이터 전송:

```python
for item in data:
    producer.send(KAFKA_TOPIC, item)
```
producer.send(KAFKA_TOPIC, item): 각 데이터를 지정된 Kafka 토픽으로 전송합니다.
- 버퍼 플러시:

```python
producer.flush()
```

producer.flush(): 버퍼에 저장된 모든 메시지를 브로커로 전송하고 확인을 받기 전까지 대기합니다.

- 주요 포인트
KafkaProducer: Kafka로 메시지를 전송하는 클라이언트 역할을 합니다.

bootstrap_servers: Kafka 클러스터의 초기 호스트 목록을 지정합니다.

value_serializer: 메시지를 직렬화하여 바이트 스트림으로 변환합니다.

send: 메시지를 비동기적으로 지정된 토픽에 전송합니다.

flush: 버퍼에 저장된 메시지를 강제로 전송하고 전송이 완료될 때까지 대기합니다.

이 코드는 주어진 데이터를 Kafka 토픽으로 전송하는 역할을 하며, 데이터가 리스트 형태로 주어져야 함을 가정하고 있습니다. 데이터가 리스트가 아닌 경우 예외를 발생시킵니다.


## Kafka Stream Consumer
이 섹션에서는 kafka_stream 함수와 Kafka Consumer 개념을 자세히 설명합니다. kafka_stream 함수는 Kafka 토픽에서 스트리밍 데이터를 읽어오는 역할을 합니다.

함수 설명
### kafka_stream

```
def kafka_stream(spark_session: SparkSession, **kwargs) -> DataFrame:
    return spark_session.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", kwargs["servers"]) \
        .option("subscribe", kwargs["topic"]) \
        .option("startingOffsets", "latest") \
        .load()
```


이 함수는 Apache Spark를 사용하여 Kafka로부터 실시간 스트리밍 데이터를 읽어오는 DataFrame을 반환합니다.


spark_session (SparkSession): SparkSession 객체.

kwargs (dict): Kafka 연결 설정을 포함한 다양한 옵션.

## Kafka Consumer 옵션
kafka.bootstrap.servers: Kafka 브로커의 주소 목록을 지정합니다. 여러 서버를 콤마로 구분하여 입력할 수 있습니다.

subscribe: 구독할 Kafka 토픽을 지정합니다.

startingOffsets: 스트리밍을 시작할 위치를 지정합니다. 일반적으로 "earliest" (가장 처음) 또는 "latest" (가장 최신) 중 하나를 선택합니다.
반환값

DataFrame: Kafka에서 읽어온 스트리밍 데이터를 포함하는 DataFrame.

## Kafka Consumer 개념
Kafka Consumer는 Kafka 토픽에서 메시지를 읽어오는 역할을 합니다. Consumer는 Producer가 보낸 메시지를 처리하고, 필요에 따라 저장하거나 다른 시스템으로 전송합니다. 이 과정은 다음과 같은 주요 개념으로 구성됩니다:

### 주요 개념
- 토픽 (Topic):

Kafka에서 데이터가 저장되는 카테고리 또는 피드 이름입니다. Producer는 특정 토픽에 메시지를 게시하고, Consumer는 해당 토픽을 구독하여 메시지를 읽어옵니다.
- 파티션 (Partition):

토픽은 하나 이상의 파티션으로 구성됩니다. 각 파티션은 메시지 순서가 보장되는 단위입니다. 파티션을 사용하여 데이터의 병렬 처리가 가능합니다.
- 오프셋 (Offset):

각 메시지는 파티션 내에서 고유한 오프셋을 가집니다. 오프셋은 메시지의 순서를 나타내며, Consumer는 오프셋을 기준으로 메시지를 읽어옵니다.
- 컨슈머 그룹 (Consumer Group):

여러 Consumer 인스턴스가 협력하여 메시지를 처리하는 그룹입니다. 각 Consumer는 동일한 그룹 내에서 각 파티션의 데이터를 독립적으로 처리합니다.
## Kafka Stream 설명
Kafka Streams는 Kafka에서 제공하는 라이브러리로, 실시간 스트리밍 데이터를 처리하고 분석하는 데 사용됩니다. Kafka Streams는 분산형 아키텍처로 설계되어 있으며, 데이터의 고가용성과 확장성을 지원합니다. 스트림 프로세싱 애플리케이션을 쉽게 개발하고 배포할 수 있게 해줍니다.

### 특징
1. 분산 처리: Kafka Streams는 분산형으로 작동하여 고가용성과 확장성을 제공합니다.
2. 상태 저장: 상태 저장 스트림 프로세싱을 지원하여, 처리 중간 결과를 저장하고 활용할 수 있습니다.
3. 실시간 처리: 실시간으로 데이터를 처리하며, 낮은 지연 시간을 보장합니다.
4. 단순한 API: 사용하기 쉬운 API를 제공하여, 복잡한 스트림 프로세싱 로직을 간단하게 구현할 수 있습니다.
### 사용 사례
1. 실시간 데이터 분석: 클릭 스트림 분석, 실시간 로그 모니터링 등.
2. ETL: 실시간 ETL(Extract, Transform, Load) 파이프라인 구축.
3. 모니터링 및 경고: 실시간 시스템 모니터링 및 이상 징후 탐지.

### kafka_stream 함수의 동작 방식
- Kafka와 연결 설정:

kafka.bootstrap.servers 옵션을 사용하여 Kafka 클러스터의 브로커 주소를 지정합니다.
- 토픽 구독:

subscribe 옵션을 사용하여 특정 토픽을 구독합니다.
- 오프셋 설정:

startingOffsets 옵션을 사용하여 스트리밍을 시작할 오프셋을 지정합니다. 여기서는 "latest"를 사용하여 가장 최신 메시지부터 읽어옵니다.
- 스트림 읽기:

spark_session.readStream.format("kafka").load()를 통해 Kafka로부터 스트리밍 데이터를 읽어옵니다. 이 데이터는 Spark DataFrame으로 반환되어, 이후의 데이터 처리 및 변환 작업에 사용됩니다.
