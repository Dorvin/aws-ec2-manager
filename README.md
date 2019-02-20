
AWS EC2 Managing Django API for Janus Server
=====================

## API guide
| path | function | method |
|:---|:---:|---:|
| `admin/` | 관리자 페이지 | GET|
| `room/make?room_name=[your room name, anything is ok]&room_code=[your room code, must be unique]` | Room 생성(새로운 aws instance) | GET |
| `room/get/<room_code>` | aws instance 의 주소를 얻기 | GET |
| `room/run/<room_code>` | aws instance 의 janus server 실행 | GET |
| `room/close/<room_code>` | aws instnace 를 종료시키기(계정당 instnace 개수 제한이 있고 돈이 들기에 반드시 사용이 끝난 후 종료시켜야함 ) | GET |

## How to run
1. Dependency
    ```
    pip3 install awscli
    pip3 install boto3
    pip3 install subprocess
    pip3 install paramiko
    ```
1. Aws cli setting
    - [aws 공식 문서 참고](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-chap-configure.html)
1. ssh 보안 설정
    - your_key_name.pem 파일을 instancemaker/your_key_name.pem 에 위치시키기
    - 8088이 열려있는(, 이외에 다른 필요한 포트들이 있다면, 그들 또한 열려있는) 보안그룹 생성(이하 yourSG)
1. 코드 수정
    - views.py를 주석에 따라 수정
1. 서버 실행
    ```
    python3 manage.py runserver
    ```