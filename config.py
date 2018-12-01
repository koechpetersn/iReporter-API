"""Application configuration."""
import os
class Config(object):
	'''Base class'''
	
class TestingConfig(Config):
    """Configuration for testing environment."""
    DEBUG = True

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = False

configurations = {
	'testing' : TestingConfig,
	'development' : DevelopmentConfig
	}