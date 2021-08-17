import json
from math import ceil
from flask import current_app
from sqlalchemy import text
from six.moves.urllib.parse import urlencode
from httplib2 import Http
from typing import Any, List, Dict, Iterable, Union

from tracker.extensions import db, openid_connect
from config.settings import client_secrets
from config.kc_admin_endpoints import (
    VIEW_USERS_URI, USER_CLIENT_ROLES_URI, VIEW_CLIENTS_URI
)


def user_activity_between_dates(from_date, to_date):
    sql = text('SELECT tr.user, \
        count(case when tr.inserted = 1 and tr.`table` = "lexicalunit" then  1 END) sense_created,\
        count(case when tr.inserted = 0 and tr.deleted = 0 and tr.`table` = "lexicalunit" then  1 END) sense_modified,\
        count(case when tr.deleted = 1 and tr.`table` = "lexicalunit" then  1 END) sense_removed, \
        count(case when tr.inserted = 1 and tr.`table` = "lexicalrelation" then  1 END) senserelation_created,\
        count(case when tr.deleted = 1 and tr.`table` = "lexicalrelation" then  1 END) senserelation_removed, \
        count(case when tr.inserted = 1 and tr.`table` = "synset" then  1 END) synset_created, \
        count(case when tr.inserted = 0 and tr.deleted = 0 and tr.`table` = "synset" then  1 END) synset_modified,\
        count(case when tr.deleted = 1 and tr.`table` = "synset" then  1 END) synset_removed,\
        count(case when tr.inserted = 1 and tr.`table` = "synsetrelation" then  1 END) synsetrelation_created,\
        count(case when tr.deleted = 1 and tr.`table` = "synsetrelation" then  1 END) synsetrelation_removed\
        FROM tracker tr WHERE DATE(tr.datetime) >= :from_date AND DATE(tr.datetime) <= :to_date AND tr.user is not null GROUP BY tr.user')
    return db.engine.execute(sql, {'from_date': from_date, 'to_date': to_date})


def user_activity_month(year, month, user):
    user = user.replace(" ", ".")
    sql = text('SELECT tr.user, \
        count(case when tr.inserted = 1 and tr.`table` = "lexicalunit" then  1 END) sense_created,\
        count(case when tr.inserted = 0 and tr.deleted = 0 and tr.`table` = "lexicalunit" then  1 END) sense_modified,\
        count(case when tr.deleted = 1 and tr.`table` = "lexicalunit" then  1 END) sense_removed, \
        count(case when tr.inserted = 1 and tr.`table` = "lexicalrelation" then  1 END) senserelation_created,\
        count(case when tr.deleted = 1 and tr.`table` = "lexicalrelation" then  1 END) senserelation_removed, \
        count(case when tr.inserted = 1 and tr.`table` = "synset" then  1 END) synset_created, \
        count(case when tr.inserted = 0 and tr.deleted = 0 and tr.`table` = "synset" then  1 END) synset_modified,\
        count(case when tr.deleted = 1 and tr.`table` = "synset" then  1 END) synset_removed,\
        count(case when tr.inserted = 1 and tr.`table` = "synsetrelation" then  1 END) synsetrelation_created,\
        count(case when tr.deleted = 1 and tr.`table` = "synsetrelation" then  1 END) synsetrelation_removed\
        FROM tracker tr WHERE YEAR(tr.datetime) = :n_year AND MONTH(tr.datetime) = :n_month AND tr.user =:user_name GROUP BY tr.user')
    return db.engine.execute(sql, {'n_year': year, 'n_month': month, 'user_name': user})


def user_activity_day(now_date):
    sql = text('SELECT tr.user, \
        count(case when tr.inserted = 1 and tr.`table` = "lexicalunit" then  1 END) sense_created,\
        count(case when tr.inserted = 0 and tr.deleted = 0 and tr.`table` = "lexicalunit" then  1 END) sense_modified,\
        count(case when tr.deleted = 1 and tr.`table` = "lexicalunit" then  1 END) sense_removed, \
        count(case when tr.inserted = 1 and tr.`table` = "lexicalrelation" then  1 END) senserelation_created,\
        count(case when tr.deleted = 1 and tr.`table` = "lexicalrelation" then  1 END) senserelation_removed, \
        count(case when tr.inserted = 1 and tr.`table` = "synset" then  1 END) synset_created, \
        count(case when tr.inserted = 0 and tr.deleted = 0 and tr.`table` = "synset" then  1 END) synset_modified,\
        count(case when tr.deleted = 1 and tr.`table` = "synset" then  1 END) synset_removed,\
        count(case when tr.inserted = 1 and tr.`table` = "synsetrelation" then  1 END) synsetrelation_created,\
        count(case when tr.deleted = 1 and tr.`table` = "synsetrelation" then  1 END) synsetrelation_removed\
        FROM tracker tr WHERE DATE(tr.datetime) = :now_date AND tr.user is not null GROUP BY tr.user')
    return db.engine.execute(sql, {'now_date': now_date})


class CurrentUser:
    """Current user representation based on ID token."""

    def __init__(self) -> None:
        self.resource_access = self._get_resource_access()
        self.client_roles = self._get_client_roles()

    def get_role(self) -> Union[str, None]:
        """Get first role of the user."""
        client_roles = self.client_roles
        if client_roles:
            return client_roles[0]
        return None

    def get_fullname(self) -> Union[str, None]:
        """Get user's full name."""
        try:
            return openid_connect.user_getfield('name')
        except Exception:
            current_app.logger.warning("Missing current user's fullname!")
            return None

    def get_firstname(self) -> Union[str, None]:
        """Get user's first name."""
        try:
            return openid_connect.user_getfield('given_name')
        except Exception:
            current_app.logger.warning("Missing current user's firstname!")
            return None

    def get_lastname(self) -> Union[str, None]:
        """Get user's last name."""
        try:
            return openid_connect.user_getfield('family_name')
        except Exception:
            current_app.logger.warning("Missing current user's lastname!")
            return None

    def get_email(self) -> Union[str, None]:
        """Get user's email address."""
        try:
            return openid_connect.user_getfield('email')
        except Exception:
            current_app.logger.warning("Missing current user's email!")
            return None

    def is_admin(self) -> bool:
        """Determines whether the user is an admin.

        Checks if user's roles contains admin role specified in configuration.
        """
        admin_role = current_app.config['KEYCLOAK_ADMIN_ROLE']
        return admin_role in self.client_roles

    def is_loggedin(self) -> bool:
        """Checks if user logged in using Flask-OIDC build in method."""
        return openid_connect.user_loggedin

    def logout(self):
        """Logout the current user.

        Clears cookie ID token data and sending request on OP's endsession endpoint.
        """
        if self.is_loggedin():
            self._send_logout_request()
            openid_connect.logout()
        else:
            current_app.logger.info(
                'Unable to log out the user. Already logged out.'
            )

    def _get_resource_access(self) -> Dict[str, Any]:
        """Get access data from OP (OpenID Connect Provider).

        Access data contains information such as client roles etc.

        Returns:
            Dict[str, Any]: Access data, None if an excepetion occured.
        """
        try:
            return openid_connect.user_getfield('resource_access')
        except Exception:
            current_app.logger.error(
                "ID token does not contain `resource_access` claim or user \
                does not have any access granted!"
            )
            return None

    def _get_client_roles(self) -> List[str]:
        """Get user's roles linked to client ID specified in configuration.

        Returns:
            List[str]: User's roles if access data exists otherwise returns
            empty list.
        """
        if self.resource_access:
            client_id = current_app.config['KEYCLOAK_CLIENT_ID']
            if client_id in self.resource_access.keys():
                roles = self.resource_access[client_id]['roles']
                if roles:
                    return roles

            current_app.logger.warning(
                'Current user does not have any %s roles!', client_id
            )

        return []

    def _send_logout_request(self):
        """Send request on OP's endsession endpoint using client credentials."""
        body_dict = {
            'client_id': current_app.config['KEYCLOAK_CLIENT_ID'],
            'client_secret': current_app.config['KEYCLOAK_CLIENT_SECRET'],
            'refresh_token': openid_connect.get_refresh_token()
        }

        response, _ = Http().request(
            uri=current_app.config['KEYCLOAK_LOGOUT_URI'],
            method='POST',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {openid_connect.get_access_token()}'
            },
            body=urlencode(body_dict)
        )

        if hasattr(response, 'status'):
            if 200 <= response.status <= 299:
                current_app.logger.info('Succesfully logged out.')
        else:
            current_app.logger.warning('Logging out failed!')

        """
        Hash a plaintext string using SHA-256 with base64 encoding.

        :param plaintext_password: Password in plain text
        :type plaintext_password: str
        :return: str
        """
        if plaintext_password:
            hash_object = hashlib.sha256(plaintext_password.encode())
            hex_dig = hash_object.digest()
            return base64.b64encode(hex_dig).decode()

        return None

    @classmethod
    def deserialize_token(cls, token):
        """
        Obtain a user from de-serializing a signed token.

        :param token: Signed token.
        :type token: str
        :return: User instance or None
        """
        private_key = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'])
        try:
            decoded_payload = private_key.loads(token)

            return User.find_by_identity(decoded_payload.get('user_email'))
        except Exception:
            return None

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query or query == '':
            return ''

        search_query = f'%{query}%'
        search_chain = (User.email.ilike(search_query),
                        User.first_name.ilike(search_query),
                        User.last_name.ilike(search_query),
                        User.id.ilike(search_query),
                        User.role.ilike(search_query))

        return or_(*search_chain)

    @classmethod
    def sort_by(cls, field, direction):
        """
        Validate the sort field and direction.

        :param field: Field name
        :type field: str
        :param direction: Direction
        :type direction: str
        :return: tuple
        """
        if field not in cls.__table__.columns:
            field = 'id'

        if direction not in ('asc', 'desc'):
            direction = 'asc'

        return field, direction

    def fullname(self):
        """
        Get user fullname
        :return: str
        """
        return self.first_name + " " + self.last_name

    def is_active(self):
        """
        Return whether or not the user account is active, this satisfies
        Flask-Login by overwriting the default value.

        :return: bool
        """
        return True

    def get_auth_token(self):
        """
        Return the user's auth token. Use their password as part of the token
        because if the user changes their password we will want to invalidate
        all of their logins across devices. It is completely fine to use
        md5 here as nothing leaks.

        This satisfies Flask-Login by providing a means to create a token.

        :return: str
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = URLSafeTimedSerializer(private_key)
        data = [str(self.id), md5(self.password.encode('utf-8')).hexdigest()]

        return serializer.dumps(data)

    def authenticated(self, with_password=True, password=''):
        """
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """

        if with_password:
            return self.password == self.encrypt_password(password)

        return True

    def serialize_token(self, expiration=3600):
        """
        Sign and create a token that can be used for things such as resetting
        a password or other tasks that involve a one off token.

        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: JSON
        """
        private_key = current_app.config['SECRET_KEY']

        serializer = TimedJSONWebSignatureSerializer(private_key, expiration)
        return serializer.dumps({'user_email': self.email}).decode('utf-8')
