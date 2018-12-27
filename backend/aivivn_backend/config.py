from datetime import timedelta
import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = True
    SECRET_KEY = 'secret_xxx'
    CACHE_DEFAULT_TIMEOUT = int(timedelta(minutes=10).total_seconds())


class ProductionConfig(Config):
    DEBUG = False
    PONY_PROVIDER = {
        'provider': 'postgres',
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'database': os.getenv('POSTGRES_DB')
    }
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT', 6379)
    CACHE_REDIS_PASSWORD = os.getenv('CACHE_REDIS_PASSWORD')
    CACHE_REDIS_DB = os.getenv('CACHE_REDIS_DB')
    SECRET_KEY = os.getenv('SECRET_KEY')


class StagingConfig(ProductionConfig):
    DEBUG = True


class DevelopmentConfig(ProductionConfig):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    PONY_PROVIDER = {
        'provider': 'sqlite',
        'filename': ':memory:',
        'create_db': True
    }
    CACHE_TYPE = 'simple'
