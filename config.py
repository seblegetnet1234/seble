"""
Configuration settings for Amharic Medical IR System
"""

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///medical_ir.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Search settings
    DEFAULT_SEARCH_LIMIT = 10
    MAX_SEARCH_LIMIT = 100
    
    # Index settings
    INDEX_PATH = os.environ.get('INDEX_PATH') or 'index'
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Use SQLite for development
    DATABASE_PATH = 'medical_ir_dev.db'
    
    # Enable debug toolbar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use environment variables for production database
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'medical_ir_prod.db'
    
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance settings
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=365)

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use in-memory database for testing
    DATABASE_PATH = ':memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])