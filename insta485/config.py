"""Insta485 development configuration."""


import pathlib


# Root of this application, useful if it doesn't
# occupy an entire domain
APPLICATION_ROOT = '/'


# Secret key for encrypting cookies
SECRET_KEY = (
    'b\xe2\xa6\xc7\x8d\xafn\x11\xe0\t\xdb\''
    'x14p\x02~\xe5\xb1lw\xfc\xeb\xf7\xb1\xb4H'
)
SESSION_COOKIE_NAME = 'login'


# File Upload to var/uploads/
INSTA485_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = INSTA485_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# Database file is var/insta485.sqlite3
DATABASE_FILENAME = INSTA485_ROOT/'var'/'insta485.sqlite3'
