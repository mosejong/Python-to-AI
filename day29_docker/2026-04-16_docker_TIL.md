# Day29 - Docker Basics and Container Practice

## 📌 오늘 배운 내용

오늘은 Docker의 기본 개념과 이미지, 컨테이너, 볼륨, 환경변수, 포트 연결을 중심으로 학습했다.  
또한 Redis, MariaDB, WordPress 컨테이너를 실행하면서 컨테이너 기반 서비스 구성을 직접 실습했다.

---

## 1. Docker 기본 개념

Docker는 애플리케이션과 실행 환경을 함께 묶어서 배포하고 실행할 수 있도록 도와주는 기술이다.

- **Image** : 실행에 필요한 환경과 파일이 포함된 패키지
- **Container** : 이미지를 실제로 실행한 결과물
- **Dockerfile** : 이미지를 만들기 위한 설정 파일

### 정리
Docker는 단순히 프로그램만 옮기는 것이 아니라,  
**프로그램이 실행될 환경까지 함께 가져가는 방식**이라고 이해할 수 있다.

---

## 2. Docker를 사용하는 이유

- 실행 환경을 통일할 수 있다
- 배포와 실행이 편리하다
- 확장과 축소가 쉽다
- 같은 이미지를 반복해서 실행할 수 있다

### 정리
내 컴퓨터와 다른 환경의 차이로 생기는 문제를 줄이기 위해 Docker를 사용한다.

---

## 3. 이미지와 컨테이너

### 흐름
```bash
Dockerfile -> build -> image -> run -> container
```

- `build` : Dockerfile을 바탕으로 이미지 생성
- `run` : 이미지를 실행해서 컨테이너 생성

### 정리
이미지는 설계도에 가깝고, 컨테이너는 실제로 실행 중인 인스턴스다.

---

## 4. 자주 사용한 Docker 명령어

### 이미지 확인
```bash
docker images
```

### 이미지 삭제
```bash
docker rmi nginx
```

### 실행 중인 컨테이너 확인
```bash
docker ps
```

### 전체 컨테이너 확인
```bash
docker ps -a
```

### 이미지 다운로드
```bash
docker pull 이미지명
```

### 컨테이너 실행
```bash
docker run 이미지명
```

### 컨테이너 삭제
```bash
docker rm 컨테이너명
```

### 컨테이너 중지
```bash
docker stop 컨테이너명
```

### 백그라운드 실행
```bash
docker run -d 이미지명
```

---

## 5. 컨테이너 내부 진입

실행 중인 컨테이너 내부로 진입할 때는 `docker exec` 명령어를 사용한다.

```bash
docker exec -it 컨테이너명 /bin/sh
```

또는

```bash
docker exec -it 컨테이너명 /bin/bash
```

### 정리
컨테이너 안에서 직접 명령어를 실행하거나 파일을 확인할 때 사용한다.

---

## 6. 환경변수

환경변수는 컨테이너 실행 시 동작에 영향을 주는 설정값이다.

예를 들면:
- 포트 번호
- DB 주소
- 사용자 이름
- 비밀번호

### 예시
```bash
docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=true mariadb
```

### 정리
환경변수는 이미지나 컨테이너가 실행될 때 필요한 설정값을 외부에서 전달하는 방법이다.

---

## 7. 볼륨과 마운트

컨테이너는 기본적으로 휘발성이 있기 때문에,  
컨테이너를 삭제하면 내부 데이터도 함께 사라질 수 있다.

이를 해결하기 위해 데이터를 외부에 저장하는 방식이 필요하며, 이를 **영속화**라고 한다.

### 방식 1. Bind Mount
- 호스트의 실제 폴더를 컨테이너에 직접 연결

### 방식 2. Volume
- Docker가 관리하는 저장 공간을 사용

### 정리
- Bind Mount는 로컬 폴더와 바로 연결되는 방식
- Volume은 Docker가 관리하는 별도 저장 공간
- 일반적으로는 Volume 방식이 더 권장된다

---

## 8. Redis 실행 실습

Redis는 메모리 기반 데이터베이스다.

### 실행 명령어
```bash
docker run --rm -p 1234:6379 redis
```

### 정리
- `--rm` : 종료 시 컨테이너 자동 삭제
- `-p 1234:6379` : 로컬 1234 포트를 컨테이너 6379 포트와 연결

이번 실습에서는 Redis 컨테이너를 실행하고,  
포트 연결을 통해 외부에서 접근 가능한 구조를 확인했다.

---

## 9. MariaDB 실행 실습

MariaDB(MySQL 계열 DB)를 Docker로 실행했다.

### 실행 명령어
```bash
docker run -d -p 3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mysql mariadb:10.9
```

### DB 접속
```bash
docker exec -it mysql mysql
```

### 데이터베이스 및 계정 생성
```sql
create database wp CHARACTER SET utf8;
grant all privileges on wp.* to wp@'%' identified by 'wp';
flush privileges;
quit
```

### 정리
- `wp` 데이터베이스를 생성
- `wp` 사용자 계정을 생성
- WordPress가 이 DB에 접속할 수 있도록 준비

---

## 10. WordPress 실행 실습

앞에서 만든 MariaDB와 연결하여 WordPress 컨테이너를 실행했다.

### 실행 명령어
```bash
docker run -d -p 8080:80 -e WORDPRESS_DB_HOST=host.docker.internal -e WORDPRESS_DB_NAME=wp -e WORDPRESS_DB_USER=wp -e WORDPRESS_DB_PASSWORD=wp wordpress
```

### 접속
```text
http://localhost:8080
```

### 정리
- 브라우저는 WordPress 컨테이너에 접속
- WordPress는 뒤에서 MariaDB에 접속
- 즉, **나 → WordPress → DB** 구조로 연결된 서비스 흐름을 확인했다

---

## 11. 실습하면서 이해한 점

- Docker는 하나의 앱만 실행하는 도구가 아니라, 여러 컨테이너를 연결해 서비스 구조를 만들 수 있다.
- WordPress와 MariaDB를 연결하면서 웹 서비스와 데이터베이스가 분리된 구조를 직접 확인할 수 있었다.
- 볼륨과 마운트는 컨테이너 데이터가 왜 사라질 수 있는지 이해하는 데 도움이 되었다.
- 환경변수는 컨테이너 실행 시 설정값을 전달하는 중요한 방법이라는 점을 알게 되었다.

---

## 어려웠던 점

- 이미지와 컨테이너 개념이 처음에는 헷갈렸다.
- 멀티 스테이지 빌드, 볼륨, 포트 연결 개념이 한 번에 들어와서 복잡하게 느껴졌다.
- 교재 예제가 리눅스 줄바꿈 기준이라 Windows cmd에서는 한 줄로 다시 입력해야 해서 처음에 헷갈렸다.

---

## 다음에 다시 볼 키워드

- Docker image / container 차이
- `docker run`, `docker ps`, `docker exec`
- 환경변수
- bind mount / volume
- WordPress와 MariaDB 연결 구조

---

## 🔍 다음 학습 예정

- Dockerfile
- 이미지 빌드 과정
- 컨테이너 실행 흐름 복습
- Docker와 Linux 개념 연결 정리