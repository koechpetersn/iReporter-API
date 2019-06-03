"""Application configuration."""

import os

class Config(object):
    """Base configurations class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    SQLALCHEMY_DATABASE_URI = os.getenv('TESTING_URL')
    DEBUG = True

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL")


configurations = {
	'development': DevelopmentConfig,
    'testing': TestingConfig
	}