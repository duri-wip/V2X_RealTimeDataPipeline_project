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
    wget https://downloads.apache.org/kafka/3.0.0/kafka_2.13-3.0.0.tgz
    tar -xzf kafka_2.13-3.0.0.tgz
    cd kafka_2.13-3.0.0
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
    log.dirs=/tmp/kafka-logs
    ```

- **ZooKeeper 연결**:
    ```properties
    zookeeper.connect=localhost:2181
    ```

## 사용법
### 토픽 생성
`my-topic`이라는 Kafka 토픽을 생성하려면:
```bash
bin/kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1
