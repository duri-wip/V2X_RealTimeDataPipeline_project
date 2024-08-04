# spark

api -> airflow -> kafka -> spark -> postgres, HDFS
prometheus -> grafana

# 스파크

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
-

### 스파크 클러스터의 구조

# 구현

## 1. 카프카 스트림 데이터를 받아오기

스키마 정의

```python
from pyspark.sql.types import StringType, DoubleType, IntegerType, LongType, StructField, StructType, TimestampType


carinfo_schema = StructType([
    StructField("dataId", StringType(), False),              # 데이터ID
    StructField("trsmDy", IntegerType(), True),              # 패킷전송일
    StructField("trmnId", StringType(), True),               # 단말기ID
    StructField("trsmUtcTime", DoubleType(), True),            # 전송UTC시간
    StructField("trsmYear", StringType(), True),            # 패킷전송년도
    StructField("trsmMt", StringType(), True),              # 패킷전송월
    StructField("trsmTm", StringType(), True),              # 패킷전송시간
    StructField("trsmMs", StringType(), True),                 # 패킷전송밀리초
    StructField("vhcleLot", DoubleType(), True),             # 차량경도
    StructField("vhcleLat", DoubleType(), True),             # 차량위도
    StructField("vhcleEvt", DoubleType(), True),            # 차량고도
    StructField("trmnTypeCd", StringType(), True),           # 단말기유형코드
    StructField("gpsUtcTime", DoubleType(), True),             # GPSUTC시간
    StructField("vhcleDrc", DoubleType(), True),            # 차량방향
    StructField("vhcleSped", DoubleType(), True),           # 차량속도
    StructField("trnsmStatCd", StringType(), True),          # 기어상태코드
    StructField("lcdtRevisnStatCd", StringType(), True),     # 측위보정상태코드
    StructField("vhcleTypeCd", StringType(), True),          # 차량유형코드
    StructField("rgtrId", StringType(), True),               # 등록자ID
    StructField("regDt", TimestampType(), True)              # 등록일시
])
```

스파크 세션 만들기

````python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark_consumer_schema import carinfo_schema

spark = SparkSession.builder.appName("test_topic_streaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3") \
    .getOrCreate()
```python

info 레벨의 로그를 출력하기.
스파크 애플리케이션의 로그 레벨을 "INFO"로 설정해 디버깅 목적으로 로그 메시지를 확인하는 경우를 대비한다.
```python
spark.sparkContext.setLogLevel("INFO")
````

## 2. 받아온 데이터를 콘솔에 출력하기

스트림데이터를 출력하기 위해서 readStream 객체를 만들어준다.

```python
car_info_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "172.31.10.193:9092") \
    .option("subscribe", "car_info") \
    .option("startingOffsets", "latest") \
    .load()
```

위에서 만든 스키마를 읽어온 스트림 데이터에 적용하고 car_info 스키마 안의 모든 열을 읽어온다.

```python
car_info_df = car_info_stream.select(from_json(col("value").cast("STRING"), carinfo_schema).alias("car_info"))
car_info_table = car_info_df.select("car_info.*")
```

콘솔에 출력하기

```python
console_print_stream = car_info_table \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

console_print_stream.awaitTermination()
```

## 3. 받아온 데이터를 postgres에 저장하기

postgres 연결 정보

```python
jdbc_url = "jdbc:postgresql://172.31.10.1:5432/team13"
properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

table_name = "car_info_table"
```

writestream에서 설정된 스키마와 postgres에서 설정된 스키마가 다른 경우 필요한 열을 선택한다.

```python
selected_columns = ["dataId", "trmnId", "vhcleLot", "vhcleLat", "gpsUtcTime", "vhcleSped", "vhcleTypeCd"]
df_selected = car_info_table.select([col for col in selected_columns])

df_renamed = df_selected \
    .withColumnRenamed("dataId", "data_id") \
    .withColumnRenamed("trmnId", "trmncd") \
    .withColumnRenamed("vhcleLot", "detclot") \
    .withColumnRenamed("vhcleLat", "detclat") \
    .withColumnRenamed("gpsUtcTime", "gpsutctime") \
    .withColumnRenamed("vhcleSped", "vhclesped") \
    .withColumnRenamed("vhcleTypeCd", "vhcletypecd")
```

스트리밍을 시작하고 PostgreSQL에 데이터 쓰기

```python
spark_to_rdbms = df_renamed.writeStream \
    .foreachBatch(lambda batch_df, batch_id:
        batch_df.write.jdbc(url=jdbc_url, table=table_name, mode="append", properties=properties)
    ) \
    .outputMode("append") \
    .trigger(processingTime='1 minute') \
    .start()

spark_to_rdbms.awaitTermination()
```

## 4. 받아온 데이터를 HDFS에 저장하기

```python
spark_to_hdfs = car_info_table.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("path", "/data/car_info/") \
    .option("checkpointLocation", "/data/car_info/check_point") \
    .trigger(processingTime = '5 seconds') \
    .start()

spark_to_hdfs.awaitTermination()
```
