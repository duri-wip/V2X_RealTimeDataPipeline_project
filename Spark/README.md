## 개요
카프카, 스파크, hdfs, postgres 를 이용하여 실시간 데이터스트림 처리 파이프라인 구축하기

### 프로젝트 소개
* 실시간으로 생성되는 대량의 데이터를 처리하고, 서버의 상태를 추적하며 문제가 발생할 경우 이를 해결하여 서버의 안정성을 향상시킬 필요성의 등장
* 대량의 실시간 데이터를 처리하기 위해 확장가능한 프레임워크, 기술을 사용한 아키텍처를 구성해야함
* 에어플로우, 카프카, 스파크, 하둡 hdfs, postgresql 등을 사용하여 실시간 데이터 파이프라인을 구축
* 데이터 시각화는 멀로 함

### 파이프라인 아키텍처

아키텍처 그림


### 사용 기술




### 환경
버전정보



# spark

api -> airflow -> kafka -> spark -> postgres, HDFS 
                prometheus -> grafana
 






# 스파크
### 스파크 스트럭트 스트림이란


### 스파크 클러스터의 구조




# 구현
## 1. 카프카 스트림 데이터를 받아오기

스키마 정의
~~~
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
~~~

스파크 세션 만들기

~~~
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark_consumer_schema import carinfo_schema

spark = SparkSession.builder.appName("test_topic_streaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3") \
    .getOrCreate()
~~~

info 레벨의 로그를 출력하기. 
스파크 애플리케이션의 로그 레벨을 "INFO"로 설정해 디버깅 목적으로 로그 메시지를 확인하는 경우를 대비한다. 
~~~
spark.sparkContext.setLogLevel("INFO")
~~~

## 2. 받아온 데이터를 콘솔에 출력하기

스트림데이터를 출력하기 위해서 readStream 객체를 만들어준다. 
~~~
car_info_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "172.31.10.193:9092") \
    .option("subscribe", "car_info") \
    .option("startingOffsets", "latest") \
    .load()
~~~


위에서 만든 스키마를 읽어온 스트림 데이터에 적용하고 car_info 스키마 안의 모든 열을 읽어온다.
~~~
car_info_df = car_info_stream.select(from_json(col("value").cast("STRING"), carinfo_schema).alias("car_info"))
car_info_table = car_info_df.select("car_info.*")
~~~

콘솔에 출력하기
~~~
console_print_stream = car_info_table \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

console_print_stream.awaitTermination()
~~~

## 3. 받아온 데이터를 postgres에 저장하기

postgres 연결 정보
~~~
jdbc_url = "jdbc:postgresql://172.31.10.1:5432/team13"
properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

table_name = "car_info_table"
~~~

writestream에서 설정된 스키마와 postgres에서 설정된 스키마가 다른 경우 필요한 열을 선택한다. 
~~~
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
~~~

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