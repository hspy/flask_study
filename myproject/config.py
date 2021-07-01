import os
#base dir == pybo
BASE_DIR = os.path.dirname(__file__)
# db_path : /home/joe/flask/myproject
# db uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False