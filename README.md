# webserber using python django
TCP로 혼잡도 받아서 뿌려주기

# accounts
- superuser
    admin/jy1234

# db tables
- Facility
  - Building
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
