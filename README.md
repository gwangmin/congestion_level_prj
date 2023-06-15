# webserber using python django
TCP로 혼잡도 받아서 뿌려주기

# accounts
- superuser
    admin/jy1234
- 제약사항: FacilityManager 계정 하나 당 담당 Facility 한 개

# db tables
- Facility(시설)
  - Building(관)
    - CCTV
- Statistics

# how to run server
- in dev
    source prepare_dev
    python manage.py runserver
- in deploy
    docker-compose build
    docker-compose up

# deploy
user request -> server docker -> nginx <-> gunicorn -> django
- deploy guide
  in screen util
  1. docker-compose down, remove images
  2. remove/clone git repo
  3. docker-compose build, up

# Server
- http://ec2-54-180-160-31.ap-northeast-2.compute.amazonaws.com/
