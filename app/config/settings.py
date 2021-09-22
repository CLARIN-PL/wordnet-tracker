import os
import json

from datetime import timedelta

# FLASK
DEBUG = False
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
KEYCLOAK_CLIENT_SECRET = os.environ.get('KEYCLOAK_CLIENT_SECRET')
KEYCLOAK_ADMIN_ROLE = os.environ.get('KEYCLOAK_ADMIN_ROLE')

KEYCLOAK_LOGOUT_URI = f'{WWW_PROTOCOL}://{KEYCLOAK_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/logout'

# Flask-OIDC
client_secrets = {
    "web": {
        "auth_uri": f"{WWW_PROTOCOL}://{SERVER_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/auth",
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "redirect_uris": [
            f"{WWW_PROTOCOL}://{SERVER_ADDRESS}:{SERVER_PORT}/oidc_callback"
        ],
        "userinfo_uri": f"{WWW_PROTOCOL}://{KEYCLOAK_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/userinfo",
        "token_uri": f"{WWW_PROTOCOL}://{KEYCLOAK_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/token",
        "token_introspection_uri": f"{WWW_PROTOCOL}://{KEYCLOAK_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}/protocol/openid-connect/token/introspect"
    }
}

OIDC_CLIENT_SECRETS = "config/client_secrets.json"
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_VALID_ISSUERS = [
    f'{WWW_PROTOCOL}://{SERVER_ADDRESS}:{KEYCLOAK_SERVER_PORT}/auth/realms/{KEYCLOAK_REALM_NAME}'
]
OIDC_OPENID_REALM = f'{WWW_PROTOCOL}://web:5000/oidc_callback'

with open(OIDC_CLIENT_SECRETS, 'w') as f:
    json.dump(client_secrets, f, indent=2)

# Api URL
API_SERVER_URL = os.environ.get('API_URL')
