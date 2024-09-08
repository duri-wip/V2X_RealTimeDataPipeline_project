# V2X 실시간 데이터 파이프라인 구축 프로젝트

## 프로젝트 소개

- 실시간으로 생성되는 대량의 데이터를 처리하고, 서버의 상태를 추적하며 문제가 발생할 경우 이를 해결하여 서버의 안정성을 향상시킬 필요성의 등장했다.
- 따라서 대량의 실시간 데이터를 처리하기 위해 확장가능한 프레임워크, 기술을 사용한 아키텍처를 구성해야한다.
- Airflow, Kafka, Spark, HDFS, PostgreSQL 등을 사용하여 실시간 데이터 파이프라인을 구축하는 것을 목적으로 프로젝트를 진행한다.
- 데이터 시각화는 Streamlit을 통해서 수행 및 배포한다.

## 파이프라인 아키텍처

![Architecture diagram](https://github.com/user-attachments/assets/b2588285-1a27-4ed2-8bbd-e9bc3e1891c6)

![Server Architecture](https://github.com/user-attachments/assets/ca6e7eba-d86b-41f5-973c-7faa745165fc)

### 사용 기술 및 환경

**링크를 통해서 자세한 내용을 확인할 수 있습니다.**

| 기술명                                                                                    | 버전정보 |
| ----------------------------------------------------------------------------------------- | -------- |
| [Hadoop & HDFS](https://github.com/leegyoungmin/data_plumber13/tree/master/hadoop%20hdfs) | 3.3.6    |
| [PostgreSQL](https://github.com/leegyoungmin/data_plumber13/tree/master/PostgreSQL)       | 16.3     |
| [Spark](https://github.com/leegyoungmin/data_plumber13/tree/master/Spark)                 | 3.5.1    |
| [Kafka](https://github.com/leegyoungmin/data_plumber13/tree/master/Kafka)                 | 2.13     |
| [Airflow](https://github.com/leegyoungmin/data_plumber13/tree/master/Airflow)             | 2.9.3    |
