# -*- coding: utf-8 -*-
"""
Configuration Module
Loads environment variables and application settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # Flask Settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'production')
    
    # Twilio Settings
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'whatsapp:+14155238886')
    
    # Application Settings
    APP_NAME = os.getenv('APP_NAME', 'SwasthyaGuide')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '1600'))
    
    # Database Settings
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    # Default to local PostgreSQL for development
    if not DATABASE_URL:
        DATABASE_URL = os.getenv(
            'DEV_DATABASE_URL',
            'postgresql://postgres:postgres@localhost:5432/swasthyaguide'
        )
    # Handle Heroku/Render postgres:// URLs
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    # Database Connection Pool Settings
    DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '10'))
    DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '20'))
    DB_POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        errors = []
        
        if not Config.SECRET_KEY or Config.SECRET_KEY == 'dev-secret-key-change-in-production':
            if Config.ENV == 'production':
                errors.append("FLASK_SECRET_KEY must be set in production")
        
        # Twilio validation only needed for production
        if Config.ENV == 'production':
            if not Config.TWILIO_ACCOUNT_SID:
                errors.append("TWILIO_ACCOUNT_SID is required")
            if not Config.TWILIO_AUTH_TOKEN:
                errors.append("TWILIO_AUTH_TOKEN is required")
        
        # Database validation
        if not Config.DATABASE_URL:
            errors.append("DATABASE_URL is required. Set it in environment variables or .env file")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True
