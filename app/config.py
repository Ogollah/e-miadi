import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


