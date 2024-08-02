### 에러 1
~~~
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
	Is the server running locally and accepting connections on that socket?
~~~
이건 처음 보는 에러인데 구글링해도 정보도 별로 없고 해결하지 못해 결국 재설치했다.

  - +) sudo systemctl status postgresql을 해보니
    ~~~
    postgresql.service - PostgreSQL RDBMS
     Loaded: loaded (/usr/lib/systemd/system/postgresql.service; enabled; preset: enabled)
     Active: active (exited) since Fri 2024-08-02 02:54:49 UTC; 1h 52min ago
    Process: 121376 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
     Main PID: 121376 (code=exited, status=0/SUCCESS)
        CPU: 1ms
    Aug 02 02:54:49 server05 systemd[1]: Starting postgresql.service - PostgreSQL RDBMS...
    Aug 02 02:54:49 server05 systemd[1]: Finished postgresql.service - PostgreSQL RDBMS.
    ~~~
    이렇게 나오는데 상태 옆에 있는 경로에 들어가서
    ~~~
    [Unit]
    Description=PostgreSQL RDBMS
    After=network.target
    [Service]
    #Type=oneshot
    #ExecStart=/bin/true
    #ExecReload=/bin/true
    #RemainAfterExit=on
    Type=simple
    User=postgres
    ExecStart=/usr/lib/postgresql/16/bin/postgres -D /var/lib/postgresql/16/main -c config_file=/etc/postgresql/16/main/postgresql.conf
    ExecReload=/bin/kill -HUP $MAINPID
    TimeoutSec=300
    Restart=always
    [Install]
    WantedBy=multi-user.target
    ~~~
    위와 같이 수정하고 sudo service postgresql restart하니 들어가졌다.


### 에러 2
standby server log를 찍으니 아래와 같이 나왔다.
~~~
cp: cannot create regular file '/var/lib/postgresql/16/archive/000000010000000000000001': Permission denied
2024-08-01 17:23:05.525 KST [56690] LOG: archive command failed with exit code 1
2024-08-01 17:23:05.525 KST [56690] DETAIL: The failed archive command was: cp pg_wal/000000010000000000000001 /var/lib/postgresql/16/archive/000000010000000000000001
~~~
권한이 없다고 해서 /tmp로 폴더를 옮겼다.


### 에러 3
main server 아카이브 폴더에 WAL파일이 들어가고 standby server log를 찍으니 아래와 같이 나왔다.
~~~
cp: cannot stat '/tmp/archive/000000010000000000000005': No such file or directory
cp: cannot stat '/tmp/archive/00000002.history': No such file or directory
2024-08-02 01:13:45.933 UTC [109795] LOG: waiting for WAL to become available at 0/5000018
~~~
확실하진 않지만 복제슬롯이 없어서 WAL파일이 standby server로 넘어가지 못한 것 같다.
