# re-deploy
0. enter screen
1. sudo docker-compose down -v
2. 도커 이미지 삭제
3. cd ..; sudo rm -rf congestion_level_prj
4. git clone https://github.com/gwangmin/congestion_level_prj.git
5. 깃헙 로긴
6. cd congestion_level_prj; sudo docker-compose build
7. sudo docker-compose up

# accounts
- superuser
    admin/jy1234
- facility manager
    fm/fm
- 제약사항: FacilityManager 계정 하나 당 담당 Facility 한 개

# Facility Manager 계정 추가하는 방법
1. python manage.py createsuperuser로 추가
2. admin 페이지에서 방금 추가한 계정 수정
3. 최상위 사용자 권한, 스태프 권한 삭제하고 facility 지정

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
- http://3.37.73.70/
