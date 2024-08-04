# Dashboard 구현방식

- JMX API를 통한 metrics 출력 및 Grafana를 이용한 모니터링 대시보드 구현
	1. Kafka와 Zookeeper
		- Kafka와 Zookeeper의 환경설정을 통한 metrics의 JMX 출력 활성화
	2. JMX Exporter
		- 버전: 1.0.1
  		- Java 애플리케이션 모니터링: JMX Exporter는 Java 애플리케이션의 내부 상태를 모니터링할 수 있도록 JMX(Java Management Extensions) 메트릭을 Prometheus 형식으로 변환하여 JVM 모니터링이 용이
   	        - 설정 파일을 통해 필요한 메트릭만 선택적으로 수집할 수 있어 메트릭을 유연하게 구성 가능
                - Java 애플리케이션과 쉽게 통합될 수 있어, 기존 시스템에 큰 변경 없이 모니터링을 구현할 수 있음
	1. Prometheus
		- 버전: 2.29.1
  		- 시계열 데이터베이스: 시계열 데이터를 저장하고 관리하는 데 최적화된 데이터베이스이므로 모니터링 데이터를 효율적으로 저장하고 쿼리할 수 있음
   	        - 다양한 메트릭 수집 가능: 다양한 방법으로 메트릭을 수집할 수 있음. Pull 모델을 사용하여 설정된 간격으로 메트릭을 수집함으로써 실시간 모니터링 가능
                - 자체 쿼리 언어인 PromQL을 제공하여 복잡한 데이터 분석 및 대시보드 생성이 용이함

	2. Grafana
		- 버전: 8.1.3
  		- 강력한 시각화 기능: 다양한 차트와 그래프 유형을 제공하여 데이터를 시각적으로 표시하기 쉽고, 이를 통해 복잡한 메트릭을 쉽게 분석 가능함
   	        - 대시보드 공유 및 관리: 대시보드 생성, 공유, 관리가 용이하여 팀 내에서 일관된 모니터링 환경을 구축할 수 있음
                - 복수의 데이터 소스 통합: Prometheus 외에도 다양한 데이터 소스를 통합할 수 있어 여러 시스템의 데이터를 한 곳에서 시각화할 수 있음

	→ JMX Exporter, Prometheus, Grafana 모두 오픈소스 프로젝트로 무료로 사용 가능하며, 커뮤니티 지원이 활발한 편으로 대시보드 구성 Application으로 채택

- 전체 대시보드([링크](http://13.125.191.32:3000/d/JtWBzWAiz/kafka-cluster-monitoring-dashboard?orgId=1&refresh=5s&from=1722743108980&to=1722744908980))
	- Kafka cluster monitoring: 카프카 클러스터 관련 지표 모니터링
	- Zookeeper monitoring: 주키퍼 관련 지표 모니터링
	- JVM monitoring: 자바 가상 머신(JVM) 관련 지표 모니터링
![](https://i.imgur.com/Bj0erHe.png)
_Kafka Cluster Monitoring Dashboard_

# Kafka cluster monitoring

- Transactions topic
	- 현재 처리 중인 토픽들의 트랜잭션 수
	- 처리 중일 때, 0보다 큰 값
  ![|](https://i.imgur.com/WnNK924.png)

- Active controller count
	- 클러스터에서 현재 활성 상태인 컨트롤러의 수
	- 컨트롤러는 클러스터 메타데이터의 변경을 관리 역할
	- 일반적으로 1개의 컨트롤러가 활성화

		![|350](https://i.imgur.com/5T9yCBy.png)

- Leader count
	- 브로커별 파티션의 리더의 수
	- 각 파티션은 하나의 리더와 여러 팔로워로 구성되며, 리더는 데이터 쓰기와 읽기를 담당
![|1000](https://i.imgur.com/8xNA4Kz.png)

  
- Car_info topic bytesin to bytesout
	- 'car_info' 토픽에 들어오고 나가는 데이터의 바이트 수를 모니터링
	- 'car_info' 토픽의 트래픽 분석 가능
![|1000](https://i.imgur.com/1NtEdwG.png)

- Total partition count
	- 클러스터 내의 총 파티션 수
	- 파티션은 Kafka가 데이터를 분산 저장하고 처리할 수 있게 하는 단위
![|350](https://i.imgur.com/SKDw60r.png)
  
- Total under replicated partition count
	- 복제본 수가 설정된 값보다 적은 파티션의 수
	- 0보다 클 경우, 데이터의 가용성과 내구성에 영향을 줄 수 있음
![|350](https://i.imgur.com/Bpjd8jx.png)
  
- Total offline partitions count
	- 오프라인 상태인 파티션의 수
	- 파티션이 오프라인 상태이면 해당 파티션의 데이터를 사용할 수 없음
![|350](https://i.imgur.com/TuCEgYm.png)
  
- Max lag in messages between follower and leader replicas
	- 리더와 팔로워 복제본 사이의 최대 메시지 지연을 표시
	- 데이터 동기화 상태를 확인하기 위한 지표표
![|1000](https://i.imgur.com/oULN4VC.png)
  
- Kafka network request metrics
	- 네트워크 요청 수
	- Kafka 클러스터 가동 시간에 따라 누적 증가
![|1000](https://i.imgur.com/qOXQvUy.png)
  
- Request handler load(%)
	- 요청 처리기의 부하를 백분율로 표시
	- 시스템의 처리 능력을 평가하는 지표
![|1000](https://i.imgur.com/ILjMqT3.png)
  
- Network processor load(%)
	- 네트워크 프로세서의 부하를 백분율로 표시
	- 네트워크 I/O 성능을 평가하는 지표
![|1000](https://i.imgur.com/XKP98ab.png)

# Zookeeper monitoring

- Average latency
	- 요청 처리의 평균 지연 시간을 표시
	- Zookeeper의 성능을 평가하는 지표
![|1000](https://i.imgur.com/MRbLWTJ.png)
  
- Watch count
	- 현재 설정된 감시자의 수
	- 감시자는 Zookeeper의 데이터 변경을 모니터링
![|1000](https://i.imgur.com/jg5qSb1.png)
  
- Zookeeper up status
	- Zookeeper 서버의 상태를 모니터링
	- 서버의 정상 작동  여부 확인

		![|400](https://i.imgur.com/gNQ6wzs.png)

- Active connections count
	- Zookeeper에 현재 활성화된 연결 수
	- 클라이언트와의 연결 상태를 평가하는 지표표
![|400](https://i.imgur.com/4WLgeRP.png)
  
- Leader election happens
	- 리더 선출이 발생한 횟수
	- 잦은 리더 선출은 클러스터의 안정성 문제를 나타낼 수 있음
![|400](https://i.imgur.com/qIviudo.png)
  
- Znode total occupied memory size
	- Zookeeper의 데이터 노드(Znode)가 차지하는 총 메모리 크기
	- Zookeeper의 메모리 사용량을 평가
![|700](https://i.imgur.com/3t2vl9C.png)
  
- Znode count
	- Zookeeper의 데이터 노드(Znode)의 총 개수
	- Zookeeper의 데이터 저장 상태를 평가
![700](https://i.imgur.com/HkrHMWN.png)
  
# JVM Monitoring

- JVM heap memory usage
	- JVM 힙 메모리 사용량을 모니터링
	- 애플리케이션의 메모리 사용 패턴을 분석하고 메모리 누수 문제를 발견할 수 있음
![|1000](https://i.imgur.com/EReOWLl.png)
  
- JVM CPU load
	- JVM의 CPU 사용률을 백분율 표시
	- 애플리케이션의 CPU 사용 상태를 평가
![|1000](https://i.imgur.com/8OBOJEm.png)
