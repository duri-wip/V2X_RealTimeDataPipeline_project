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
Kafka Producer는 Apache Kafka로 데이터를 전송하는 역할을 합니다. 이 프로듀서는 Kafka 클러스터의 브로커에 메시지를 보내어 특정 토픽에 데이터를 게시합니다. 코드 내에서 KafkaProducer 클래스는 다음과 같은 방식으로 사용됩니다:

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
