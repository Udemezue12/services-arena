import os
from datetime import timedelta

from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv


load_dotenv()
salt = os.getenv('SALT')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 587
    WTF_CSRF_ENABLED = True 
    MAIL_USE_TLS = True
    MAIL_USEE_SSL = False
    MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SALT = os.getenv('SALT')
    # PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
    # PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
    # TERMII_API_KEY = os.getenv('TERMII_API_KEY')
    # TERMII_MAIL_URL = os.getenv('TERMII_MAIL_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_SESSION_FOR_NEXT = True
    REMEMBER_COOKIE_DURATION = timedelta(seconds=20)

    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


# with app.app_context():
#     pass

serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'), salt)
