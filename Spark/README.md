# 스파크

### 스파크 등장 배경

- 2005년 하드웨어의 성능 향상이 중단
- 기존의 단일 프로세서로 구동되던 애플리케이션은 느려지기 시작
- 병렬 처리가 필요하게 됨
- 결과적으로 데이터 수집 비용은 극히 저렴해졌으나 데이터는 클러스터에서 처리해야 할만큼 거대해짐.

### 스파크 스트럭트 스트림이란

- 2012년 부터 map과 reduce를 지원하면서 스트림 처리가 가능해짐.
- DStream이라는 저수준 API를 활용함.
- 저수준 연산만 사용할 수 있기 때문에 최적화 기법을 활용하는 데 한계가 있었음.
- 2016년 스파크 개발자들이 DataFrame을 기반으로 새로운 API(Structured Stream)를 구축함.
- 이를 통해서 개발자 친화적으로 빠른 스트리밍 처리가 가능하게 됨.

#### 스트림 처리란?

스트림 처리는 신규 데이터를 끊임없이 처리해 결과를 만들어내는 행위입니다. 입력 데이터는 무한하게 생성되며, 시작과 끝을 정의하지 않는다.

#### 스트림 애플리케이션이란?

- 이벤트 스트림이 도착한 후 다양한 쿼리 연산을 수행
- 예를 들어 이벤트의 타입별 카운트를 추적하거나 시간별로 이벤트의 타입별 실행 카운트를 집계
- 고정된 입력 데이셋을 처리하는 배치 처리와 비교 가능
  - 배치 처리는 고정된 입력 데이터를 일반적인 애플리케이션에서 처리한다.
  - 스트림 처리는 무한한 입력 데이터를 스트리밍 애플리케이션에서 처리한다.

#### 스트림 처리의 장점

- 대기 시간이 짧기 때문에 사용자 애플리케이션이 빠르게 응답할 수 있다.
- 자동으로 연산결과를 증분 생산하기 때문에 배치 작업보다 결과를 수정하는 데 효율적이다.
- 배치 작업으로 실행하는 경우 모든 데이터를 읽어야 하지만, 스트림처리는 연산을 기억하기 때문에 용이

#### 스트림 처리의 과제

- 하나의 입력 데이터가 지연되거나 재전송되면 시간이 뒤섞여서 도착한다는 것이다.
- 대규모의 상태 정보 유지
- 높은 데이터 처리량 보장하기
- 장애 상황에서도 정확히 한번 처리하기
- 부하 불균형과 뒤처진 서버 다루기
- 이벤트에 빠르게 응답하기

#### 스트림 처리의 구분

##### 연속형 처리

- 다른 노드에서 전송하는 메시지를 끊임없이 수신하고 새로 갱신된 정보를 자신의 하위 노드로 전송
- 연속형 처리는 레코드 별로 데이터를 처리한다는 것이다.
- 연속형 처리는 신규 메시지에 즉시 반응하기 때문에 입력량이 적을 때 가장 빠르게 응답한다.
- 레코드 단위 부하가 크기 때문에 최대 처리량이 작다.

##### 마이크로 배치 처리

- 입력 데이터를 작은 배치로 모으기 위해 대기합니다.
- 배치 잡 실행 방식과 유사하게 다수의 분산 Task를 사용해 각 배치를 병렬로 처리한다.
- 더 적은 노드로 같은 양의 데이터를 처리할 수 있습니다.
- 워크로드 변화에 대응할 수 있도록 Task 수를 늘리거나 줄이는 방식인 부하 분산 기술을 동원할 수 있다.
- 배치를 모으기 위한 시간이 필요하므로 지연 시간이 발생한다.

### 스파크 클러스터

#### 구성 요소

- 드라이버 : 애플리케이션 실행을 제어하고 클러스터의 모든 상태 정보를 유지한다. 물리적 컴퓨팅 자원의 확보와 익스큐터 실행을 위해 클러스터 매지니저와 통신한다.
- 익스큐터 : 드라이버가 할당한 태스크를 수행하는 프로세스. 할당 받은 태스크를 실행하고 상태와 결과를 보고.
- 클러스터 매니저 : 드라이버, 워커의 개념을 가지고 있는데, 물리적 머신에 연결되는 개념이라는 점에서 스파크 드라이버, 익스큐터와 구분된다.

#### 스파크 지원 매니저의 종류

- 스탠드얼론 클러스터 매니저
- 아파치 mesos
- 하둡 YARN

### 스탠드얼론 매니저 (Standalone Manager)

#### 장점

- 간단한 설정 : 스탠드얼론 모드는 설정이 간단하고 빠르게 배포할 수 있습니다. 별도의 클러스터 매니저를 설치할 필요가 없고, 스파크 자체만으로 클러스터를 구성할 수 있습니다.
- 스파크 전용 : 스탠드얼론 모드는 스파크 전용 클러스터 매니저로서, 스파크 애플리케이션의 요구사항에 최적화되어 있습니다. 따라서 스파크 애플리케이션 실행에 필요한 자원을 보다 효율적으로 관리할 수 있습니다.
- 경량화 : YARN에 비해 경량화되어 있으며, 비교적 적은 자원으로도 클러스터를 운영할 수 있습니다.

#### 단점

- 자원 관리 제한 : 다른 클러스터 매니저와 비교했을 때 자원 관리는 다소 제한적입니다. 특히, 여러 애플리케이션을 동시에 실행할 때 자원 할당이 비효율적일 수 있습니다.
- 확장성 제한 : 대규모 클러스터에서 확장성 면에서 한계가 있을 수 있습니다. 많은 노드와 애플리케이션을 관리하기에는 적합하지 않을 수 있습니다.
- 다른 시스템과의 통합 부족 : YARN 같은 경우에는 Hadoop 생태계와의 통합이 용이하지만, 스탠드얼론 모드는 이러한 통합 기능이 부족합니다.

### YARN (Yet Another Resource Negotiator)

#### 장점

- 자원 관리 : YARN은 자원 관리와 스케줄링이 뛰어나며, 여러 애플리케이션이 자원을 효율적으로 공유할 수 있습니다. 자원 할당, 우선순위 지정, 큐 관리 등이 가능합니다.-
- 확장성 : 대규모 클러스터에서도 안정적으로 동작하며, 수백에서 수천 대의 노드를 쉽게 관리할 수 있습니다.
- Hadoop 생태계와의 통합 : YARN은 Hadoop의 자원 관리 프레임워크이기 때문에 Hadoop 에코시스템 내의 다른 도구들과 원활하게 통합됩니다. 특히 HDFS와의 연동이 매우 자연스럽습니다.
- 다양한 워크로드 관리 : YARN은 스파크뿐만 아니라 MapReduce, Tez 등 다양한 워크로드를 동시에 관리할 수 있습니다.

#### 단점

- 복잡한 설정 : YARN 설정은 복잡하고, YARN 클러스터를 설치하고 관리하는 데 많은 노력이 필요합니다. 설정 파일과 구성 요소가 많아 초기에 설정하는 데 시간이 걸릴 수 있습니다.
- 오버헤드 : YARN 자체가 복잡하고 다양한 기능을 제공하기 때문에 운영 오버헤드가 발생할 수 있습니다. 이는 성능에 영향을 미칠 수 있습니다.
- 의존성 : YARN을 사용하려면 Hadoop을 설치하고 유지 관리해야 하므로, 추가 관리 작업이 필요하다.

## 실행 모드

- 클러스터 모드
  - 컴파일된 jar 파일, 파이썬 스크립트, R 스크립트를 클러스터 매니저에 전달
  - 클러스터 워커에 드라이버와 익스큐터 프로세스를 실행함.
- 클라이언트 모드
  - 스파크 드라이버 프로세스를 유지하며 클러스터 매니저는 익스큐터 프로세스를 유지함.
  - 드라이버는 클러스터 외부의 머시에서 실행되며 나미저 워커는 클러스터에 위치한다.
- 로컬 모드
  - 스파크 애플리케이션을 단일 머신에게 수행하게 되며 병렬처리를 위해 스레드를 사용하게 된다.
  - 운영용 애플리케이션을 실행할 때는 권장되지 않음.
  - 개발중인 애플리케이션을 반복 실험하거나 테스트하는 용으로 사용됨.

# 구현

## 1. 카프카 스트림 데이터를 받아오기

스키마 정의

```python
from pyspark.sql.types import StringType, DoubleType, IntegerType, LongType, StructField, StructType, TimestampType

car_info_schema_for_json = StructType(
    [
        StructField("dataId", StringType(), False),                 # 데이터ID
        StructField("trsmDy", IntegerType(), True),                 # 패킷전송일
        StructField("trmnId", StringType(), True),                  # 단말기ID
        StructField("trsmUtcTime", DoubleType(), True),             # 전송UTC시간
        StructField("vhcleLot", DoubleType(), True),                # 차량경도
        StructField("vhcleLat", DoubleType(), True),                # 차량위도
        StructField("vhcleEvt", DoubleType(), True),                # 차량고도
        StructField("trmnTypeCd", StringType(), True),              # 단말기유형코드
        StructField("gpsUtcTime", DoubleType(), True),              # GPSUTC시간
        StructField("vhcleDrc", DoubleType(), True),                # 차량방향
        StructField("vhcleSped", DoubleType(), True),               # 차량속도
        StructField("trnsmStatCd", StringType(), True),             # 기어상태코드
        StructField("lcdtRevisnStatCd", StringType(), True),        # 측위보정상태코드
        StructField("vhcleTypeCd", StringType(), True)              # 등록일시
        StructField("addr", StringType(), True)                     # 시도구
    ]
)
```

스파크 세션 만들기

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark_consumer_schema import carinfo_schema

spark = SparkSession.builder.appName("test_topic_streaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3") \
    .getOrCreate()
```

info 레벨의 로그를 출력하기.

스파크 애플리케이션의 로그 레벨을 "INFO"로 설정해 디버깅 목적으로 로그 메시지를 확인하는 경우를 대비한다.

```python
spark.sparkContext.setLogLevel("INFO")
```

## 2. 받아온 데이터를 콘솔에 출력하기

### 1. 스파크 세션을 생성한다.

```python
def generate_session(app_name: str, **kwargs) -> SparkSession:
    config = SparkConf()
    check_point_path = "/home/ubuntu/app/spark-3.5.1-bin-hadoop3/check_point/"
    context = SparkContext(appName=app_name, conf=config)
    context.setCheckpointDir(check_point_path)
    context.setLogLevel(kwargs["log_level"])

    return SparkSession(sparkContext=context) \
        .builder \
        .config("spark.jars.packages", kwargs["packages"]) \
        .getOrCreate()
```

### 2. 스트림데이터를 출력하기 위해서 readStream 객체를 만들어준다.

```python
def kafka_stream(spark_session: SparkSession, **kwargs) -> DataFrame:
    return spark_session.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", kwargs["servers"]) \
        .option("subscribe", kwargs["topic"]) \
        .option("startingOffsets", "latest") \
        .load()
```

### 3. 위에서 만든 스키마를 읽어온 스트림 데이터에 적용하고 car_info 스키마 안의 모든 열을 읽어온다.

```python
car_info_table = read_stream.select(
    from_json(
        col("value").cast("STRING"),
        car_info_schema_for_json
    )
    .alias("car_info")
).select("car_info.*")
```

### 4.1 콘솔에 출력하기

```python
def logging_query(df: DataFrame, **kwargs) -> StreamingQuery:
    return df.writeStream \
        .format(kwargs["format"]) \
        .outputMode(kwargs["output"]) \
        .start()

log_query = logging_query(car_info_table, format="console", output="append")

log_query.awaitTermination()
```

### 4.2 받아온 데이터를 postgres에 저장하기

1. postgres 연결 정보

```python
jdbc_url = "jdbc:postgresql://172.31.10.1:5432/team13"
properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

table_name = "car_info_table"
```

2. writestream에서 설정된 스키마와 postgres에서 설정된 스키마가 다른 경우 필요한 열을 선택한다.

```python
selected_columns = ["dataId", "trmnId", "vhcleLot", "vhcleLat", "gpsUtcTime", "vhcleSped", "vhcleTypeCd", "addr"]
renamed_columns = ["data_id", "trmncd", "detclot", "detclat", "gpsutctime", "vhclesped", "vhcletypecd", "addr"]
selected_df = df.select(
        [col(selected).alias(renamed) for selected, renamed in zip(selected_columns, renamed_columns)]
    )
```

3. 스트리밍을 시작하고 PostgreSQL에 데이터 쓰기

```python
def insert_postgres(df: DataFrame) -> StreamingQuery:
    return df.writeStream \
        .foreachBatch(
            lambda batch_df, batch_id: batch_df.write.jdbc(
                url=jdbc_url,
                table=table_name,
                mode="append",
                properties=properties
            )
        ) \
        .outputMode("append") \
        .trigger(processingTime='1 minute') \
        .start()

save_query = save_parquet_query(
    car_info_table,
    format="parquet",
    output="append",
    path="/data/car_info/",
    check_point="/data/car_info/check_point"
)
save_query.awaitTermination()
```

### 4.3 받아온 데이터를 HDFS에 저장하기

```python
def save_parquet_query(df: DataFrame, **kwargs) -> StreamingQuery:
    time = datetime.datetime.now()
    temp_date_str = time.strftime("%y%m%d")

    return df.writeStream \
        .format(kwargs["format"]) \
        .outputMode(kwargs["output"]) \
        .option("path", kwargs["path"] + temp_date_str) \
        .option("checkpointLocation", kwargs["check_point"]) \
        .trigger(processingTime='1 minutes') \
        .start()

insert_query = insert_postgres(car_info_table)
insert_query.awaitTermination()
```
