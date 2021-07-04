import os
#base dir == pybo
BASE_DIR = os.path.dirname(__file__)
# db_path : /home/joe/flask/myproject
# db uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev" # 개발모드이므로 CSRF 토큰을 사용하지 않음