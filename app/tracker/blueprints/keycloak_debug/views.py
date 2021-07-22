from flask import Blueprint, current_app, url_for

from tracker.extensions import openid_connect
from flask_oidc.discovery import discover_OP_information


keycloak_debug = Blueprint(
    'keycloak_debug', __name__, url_prefix="/keycloak/DEBUG"
)


@keycloak_debug.route('/')
def home():
    return f'''
        <h1>Keycloak home</h1><br>
        <a href={url_for('keycloak_debug.user_info')}>/user/info</a><br>
        <a href={url_for('keycloak_debug.token')}>/token</a><br>
        <a href={url_for('keycloak_debug.op_info')}>/OP/info</a><br>
        <a href={url_for('keycloak_debug.private')}>/private</a>
        <hr>
    '''


@keycloak_debug.route('/user/info')
@openid_connect.require_login
def user_info():
    fields = ['name', 'given_name', 'family_name', 'email', 'resource_access']
    user_info = openid_connect.user_getinfo(fields)

    return f'''
        <h1>Keycloak user info</h1><br>
        <a href={url_for('keycloak_debug.home')}><b>/keycloak</b></a><br>
        <a href={url_for('keycloak_debug.token')}>/token</a><br>
        <a href={url_for('keycloak_debug.op_info')}>/OP/info</a><br>
        <a href={url_for('keycloak_debug.private')}>/private</a>
        <hr>
        {user_info}
    '''


@keycloak_debug.route('/token')
@openid_connect.require_login
def token():
    access_token = openid_connect.get_access_token()
    cookie_id_token = openid_connect.get_cookie_id_token()

    return f'''
        <h1>Keycloak token</h1><br>
        <a href={url_for('keycloak_debug.user_info')}>/user/info</a><br>
        <a href={url_for('keycloak_debug.op_info')}>/OP/info</a><br>
        <a href={url_for('keycloak_debug.private')}>/private</a>
        <hr>
        <h4>Access token:</h4>
        {access_token}
        <h4>Cookie ID token:</h4>
        {cookie_id_token}
    '''


@keycloak_debug.route('/OP/info')
def op_info():
    port = current_app.config["KEYCLOAK_SERVER_PORT"]
    realm_name = current_app.config["KEYCLOAK_REALM_NAME"]
    op_info = discover_OP_information(
        f'http://keycloak:{port}/auth/realms/{realm_name}'
    )
    content = f'''
        <h1>Keycloak OP info</h1><br>
        <a href={url_for('keycloak_debug.user_info')}>/user/info</a><br>
        <a href={url_for('keycloak_debug.token')}>/token</a><br>
        <a href={url_for('keycloak_debug.private')}>/private</a>
        <hr>
    '''
    for key, value in zip(op_info.keys(), op_info.values()):
        content += f'<b>{key}:</b><br>{"&nbsp"*4} {value}<br>'

    return content


@keycloak_debug.route('/private')
@openid_connect.require_login
def private():
    return f'''
        <h1>Keycloak private</h1><br>
        <a href={url_for('keycloak_debug.user_info')}>/user/info</a><br>
        <a href={url_for('keycloak_debug.token')}>/token</a><br>
        <a href={url_for('keycloak_debug.op_info')}>/OP/info</a><br>
        <hr>
        Private
    '''
