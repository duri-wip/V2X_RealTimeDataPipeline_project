from pyspark.sql.types import StringType, DoubleType, IntegerType, LongType, StructField, StructType, TimestampType

car_info_schema_for_json = StructType([
    StructField("dataId", StringType(), False),                 # 데이터ID
    StructField("trsmDy", IntegerType(), True),                 # 패킷전송일
    StructField("trmnId", StringType(), True),                  # 단말기ID
    StructField("trsmUtcTime", DoubleType(), True),             # 전송UTC시간
    StructField("trsmYear", StringType(), True),                # 패킷전송년도
    StructField("trsmMt", StringType(), True),                  # 패킷전송월
    StructField("trsmTm", StringType(), True),                  # 패킷전송시간
    StructField("trsmMs", StringType(), True),                  # 패킷전송밀리초
    StructField("vhcleLot", DoubleType(), True),                # 차량경도
    StructField("vhcleLat", DoubleType(), True),                # 차량위도
    StructField("vhcleEvt", DoubleType(), True),                # 차량고도
    StructField("trmnTypeCd", StringType(), True),              # 단말기유형코드
    StructField("gpsUtcTime", DoubleType(), True),              # GPSUTC시간
    StructField("vhcleDrc", DoubleType(), True),                # 차량방향
    StructField("vhcleSped", DoubleType(), True),               # 차량속도
    StructField("trnsmStatCd", StringType(), True),             # 기어상태코드
    StructField("lcdtRevisnStatCd", StringType(), True),        # 측위보정상태코드
    StructField("vhcleTypeCd", StringType(), True),             # 차량유형코드
    StructField("rgtrId", StringType(), True),                  # 등록자ID
    StructField("regDt", TimestampType(), True),                # 등록일시
    StructField("addr", StringType(), True)                     # 시도구
])