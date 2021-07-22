# flake8: noqa

import os
import json

from datetime import timedelta

# FLASK
DEBUG = False  # celery workers may not work correctly if DEBUG=True, possible conflict with flask reloader
DEBUG_TB_ENABLED = False
DEBUG_TB_HOSTS = 'localhost'
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEFAULT_CHARSET = 'utf-8'

LOG_LEVEL = 'DEBUG'

SERVER_NAME = os.environ.get('SERVER_NAME')
SERVER_ADDRESS = SERVER_NAME.split(':')[0]
SERVER_PORT = SERVER_NAME.split(':')[-1]
WWW_PROTOCOL = "http"

REMEMBER_COOKIE_DURATION = timedelta(minutes=30)
SECRET_KEY = '!$flhgsdf324NO%$#SOET!$!'

# Keycloak
KEYCLOAK_ADDRESS = os.environ.get('KEYCLOAK_ADDRESS')
KEYCLOAK_SERVER_PORT = os.environ.get('KEYCLOAK_SERVER_PORT')
KEYCLOAK_REALM_NAME = os.environ.get('KEYCLOAK_REALM_NAME')
KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID')
KEYCLOAK_ADMIN_ROLE = os.environ.get('KEYCLOAK_ADMIN_ROLE')

# Flask-OIDC
client_secrets = {
    "web": {
        "auth_uri": f"{WWW_PROTOCOL}://{SERVER_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/auth",
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": SECRET_KEY,
        "redirect_uris": [
            f"{WWW_PROTOCOL}://{SERVER_ADDRESS}:{SERVER_PORT}/oidc_callback"
        ],
        "userinfo_uri": f"{WWW_PROTOCOL}://{KEYCLOAK_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/userinfo",
        "token_uri": f"{WWW_PROTOCOL}://{KEYCLOAK_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/token",
        "token_introspection_uri": f"{WWW_PROTOCOL}://{KEYCLOAK_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/token/introspect"
    }
}

OIDC_CLIENT_SECRETS = "config/client_secrets.json"
OIDC_ID_TOKEN_COOKIE_SECURE = True
OIDC_VALID_ISSUERS = [
    f'{WWW_PROTOCOL}://{SERVER_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}'
]
OIDC_OPENID_REALM = f'{WWW_PROTOCOL}://web:5000/oidc_callback'

with open(OIDC_CLIENT_SECRETS, 'w') as f:
    json.dump(client_secrets, f, indent=2)


# SQL ALCHEMY
mysql_uri_template = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}'
SQLALCHEMY_DATABASE_URI = mysql_uri_template.format(**{
    'user': os.environ['MYSQL_USERNAME'],
    'password': os.environ['MYSQL_PASSWORD'],
    'host': os.environ['MYSQL_HOST'],
    'port': os.environ['MYSQL_PORT'],
    'db_name': os.environ['MYSQL_DATABASE'],
    'charset': 'utf8',
})

SQLALCHEMY_BINDS = {
    'users': mysql_uri_template.format(**{
        'user': os.environ['MYSQL_USERNAME'],
        'password': os.environ['MYSQL_PASSWORD'],
        'host': os.environ['MYSQL_HOST'],
        'port': os.environ['MYSQL_PORT'],
        'db_name': os.environ['MYSQL_USERS_DATABASE'],
        'charset': 'utf8',
    })
}

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# CELERY
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

ADMIN_QUERY_TASK_PERIOD = os.environ.get("ADMIN_QUERY_TASK_PERIOD")
ADMIN_QUERY_TASK_EXPIRE = os.environ.get("ADMIN_QUERY_TASK_EXPIRE")
ADMIN_QUERY_CACHE_TIMEOUT = os.environ.get("ADMIN_QUERY_CACHE_TIMEOUT", 6*3600)

CELERYBEAT_MAX_LOOP_INTERVAL = os.environ.get("CELERYBEAT_MAX_LOOP_INTERVAL", 300)  # 300 is library default
