# Hadoop Cluster 구축 목적

- Data pipeline에서 처리된 대용량 데이터를 장기적으로 백업할 수 있는 고가용 storage가 필요
    - Kafka → Spark를 통해 가공된 데이터 → Postgres와 Hadoop HDFS에 백업
        - Postgres: Data Scientist의 가공된 데이터 접근 보장
        - Hadoop HDFS: 가공된 데이터의 장기 백업 스토리지로 활용
- Hadoop Distributed File System 이용으로 대용량 데이터 읽기 / 쓰기와 데이터 유실 방지 도모

# Hadoop Cluster Architecture

- Hadoop release version: 3.3.6(2023. 6.23.)
    - Minor revision 중 가장 최신 Bug fix release → 3.4.0(2024. 5. 17) 버전 보다 안정적일 것으로 예상
    - OpenJDK 8 기반 구축
- 3 NameNodes [Server 01, 02, 03]
    - 전체 HDFS에 대한 Namespace 관리 노드
    - Datanode로 부터 block report를 받음
    - 데이터에 대한 replication 유지를 위한 commander 역할 수행
    - File system 이미지 파일(Fsimage) 관리
        - Fsimage: Namespace와 block 정보
    - File system에 대한 Edit log(edits) 관리
        - Edits: 파일의 생성, 삭제에 대한 트랜잭션 로그(메모리에 저장하다가 주기적으로 생성)
    - 고가용성 보장을 위한 3개의 NameNode 구성
- 3 DataNodes [Server 04, 05, 06]
    - 물리적으로 로컬 파일 시스템에 HDFS 데이터 저장
    - DataNode Block Scanner: NameNode가 시작될 때와 주기적으로 로컬 파일 시스템에 있는 모든 HDFS Block들을 검사 후 정상적인 block의 목록 생성 후 NameNode에 전송 → Block report
    - 고가용성 보장을 위한 3개의 DataNode 구성
        - 각 데이터 블록의 복제본 수: 2(`dfs.replication` 옵션값 = 2)
![Hadoop Cluster Architecture|700](https://i.imgur.com/X6vszoQ.png)

_Hadoop Cluster Architecture_

# Hadoop HDFS Structure

- Hadoop cluster 내 HDFS 디렉터리 구조
    - `/data` : 클러스터에서 생성된 데이터가 저장되는 디렉터리
        - `/car_info` : Spark cluster에서 처리된 차량 관련 데이터가 저장되는 디렉터리
            - `/240806` , `/240807` , … : Spark cluster에서 처리된 차량 위치 / 속도 데이터가 parquet 형식으로 저장되는 디렉터리
                - `/_spark_metadata` : Spark Structured Dataframe을 통한 Data streaming 시, 생성되는 메타 데이터 저장 디렉터리
            - `/check_point` : Spark cluster 종료 또는 장애 발생 이후 작업을 재개하기 위한 데이터가 저장되는 디렉터리
    - `/user` : HDFS user 관련 데이터가 저장되는 디렉터리
        - `/ubuntu/.Trash` : HDFS에서 파일 삭제 시, 설정 기간동안 보관 후 삭제되는 휴지통 디렉터리 (설정값: `fs.trash.interval` = 1440[분, = 24시간])

![Hadoop HDFS Structure|450](https://i.imgur.com/3TjCld0.png)

_Hadoop HDFS Structure_
