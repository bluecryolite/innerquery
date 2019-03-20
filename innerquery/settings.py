import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig():
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY = 'secret key'
    EXCEL_DOWNLOAD_PATH = os.path.join(basedir, 'innerquery/static')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # MSSQL_TARGET = {
    #     'host':'127.0.0.1',
    #     'port': 3433,
    #     'user':'dbuser',
    #     'password':'dbpassword',
    #     'database':'dbname'
    # }

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = \
        prefix + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_BINDS = {
       'target':prefix + os.path.join(basedir, 'otherdata.db')
    }

class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = \
        prefix + os.path.join(basedir, 'data.db')
    SQLALCHEMY_BINDS = {
       'target':prefix + os.path.join(basedir, 'otherdata.db')
    }

config = {'development':DevelopmentConfig,
          'production':ProductConfig}