from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.streaming import StreamingQuery

from schemas.car_info_origin_schema import car_info_schema_for_json

import datetime

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


def kafka_stream(spark_session: SparkSession, **kwargs) -> DataFrame:
    return spark_session.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", kwargs["servers"]) \
        .option("subscribe", kwargs["topic"]) \
        .option("startingOffsets", "latest") \
        .load()


def logging_query(df: DataFrame, **kwargs) -> StreamingQuery:
    return df.writeStream \
        .format(kwargs["format"]) \
        .outputMode(kwargs["output"]) \
        .start()


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


def insert_postgres(df: DataFrame) -> StreamingQuery:
    properties = {
        "user": "postgres",
        "password": "postgres",
        "driver": "org.postgresql.Driver"
    }
    jdbc_url = "jdbc:postgresql://172.31.10.1:5432/team13"

    table_name = "car_info_table"

    selected_columns = ["dataId", "trmnId", "vhcleLot", "vhcleLat", "gpsUtcTime", "vhcleSped", "vhcleTypeCd", "addr"]
    renamed_columns = ["data_id", "trmncd", "detclot", "detclat", "gpsutctime", "vhclesped", "vhcletypecd", "addr"]
    selected_df = df.select(
        [col(selected).alias(renamed) for selected, renamed in zip(selected_columns, renamed_columns)]
    )

    return selected_df.writeStream \
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


if __name__ == "__main__":
    session = generate_session(
        "car_info_streaming",
        log_level="INFO",
        packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3"
    )

    read_stream = kafka_stream(
        session,
        servers="172.31.10.193:9092,172.31.12.52:9092,172.31.0.163:9092",
        topic="car_info"
    )

    car_info_table = read_stream.select(
        from_json(
            col("value").cast("STRING"),
            car_info_schema_for_json
        )
        .alias("car_info")
    ).select("car_info.*")

    log_query = logging_query(car_info_table, format="console", output="append")
    save_query = save_parquet_query(
        car_info_table,
        format="parquet",
        output="append",
        path="/data/car_info/",
        check_point="/data/car_info/check_point"
    )
    insert_query = insert_postgres(car_info_table)

    log_query.awaitTermination()
    save_query.awaitTermination()
    insert_query.awaitTermination()
