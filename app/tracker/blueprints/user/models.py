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


class KeycloakServiceClient:
    """App service account client."""

    def __init__(self) -> None:
        self.service_access_token = self.get_service_access_token()
        self.bearer_auth_header = {
            'Authorization': f'Bearer {self.service_access_token}'
        }
        self.client_uuid = self.get_client_uuid()

        if self.service_access_token is None:
            current_app.logger.error(
                'Missing access token in `%s` object', self.__class__.__name__
            )

        if self.client_uuid is None:
            current_app.logger.error(
                'Missing client uuid in `%s` object', self.__class__.__name__
            )

    def get_realm_users(self) -> List[Dict[str, Any]]:
        """Get list of all realm users.

        Receive list of realm user representations from OP's view users
        endpoint GET request.

        Returns:
            List[Dict[str, Any]]: List of realm user representations,
            empty list if response is unsuccessful.
        """
        uri = VIEW_USERS_URI.format(
            hostname=current_app.config['KEYCLOAK_ADDRESS'],
            port=current_app.config['KEYCLOAK_SERVER_PORT'],
            realm_name=current_app.config['KEYCLOAK_REALM_NAME'],
        )

        response, content = Http().request(
            uri=uri,
            method='GET',
            headers=self.bearer_auth_header
        )

        if self._successful_response(response):
            realm_users = json.loads(content.decode('utf-8'))
            return realm_users

        return []

    def get_client_uuid(self) -> Union[str, None]:
        """Get client_uuid (not clientId!)

        Parse client UUID from client representation received from OP's view
        clients endpoint GET request.

        Returns:
            Union[str, None]: Client UUID, None if response is unsuccessful.
        """
        uri = VIEW_CLIENTS_URI.format(
            hostname=current_app.config['KEYCLOAK_ADDRESS'],
            port=current_app.config['KEYCLOAK_SERVER_PORT'],
            realm_name=current_app.config['KEYCLOAK_REALM_NAME']
        ) + f"?clientId={current_app.config['KEYCLOAK_CLIENT_ID']}"

        response, content = Http().request(
            uri=uri,
            method='GET',
            headers=self.bearer_auth_header
        )

        if self._successful_response(response):
            client_representation = json.loads(content.decode('utf-8'))
            if 'id' in client_representation[0].keys():
                client_uuid = client_representation[0]['id']
                return client_uuid

        return None

    def get_client_role_by_id(self, user_id) -> Union[str, None]:
        """Get user's client role by id.

        Parse name of the first client role from OP's clients role-mappings
        endpoint GET request.

        Returns:
            Union[str, None]: Client UUID, None if response is unsuccessful.
        """
        uri = USER_CLIENT_ROLES_URI.format(
            hostname=current_app.config['KEYCLOAK_ADDRESS'],
            port=current_app.config['KEYCLOAK_SERVER_PORT'],
            realm_name=current_app.config['KEYCLOAK_REALM_NAME'],
            user_id=user_id,
            client_uuid=self.client_uuid
        )

        response, content = Http().request(
            uri=uri,
            method='GET',
            headers=self.bearer_auth_header
        )

        if self._successful_response(response):
            user_client_roles = json.loads(content.decode('utf-8'))
            if user_client_roles:
                return user_client_roles[0]['name']

        return None

    def get_service_access_token(self) -> Union[str, None]:
        """Get service access token.

        Receive access token from OP's access token endpoint POST request using
        client credentials granty type.

        Returns:
            Union[str, None]: Access token, None if response is unsuccessful.
        """
        body_dict = {
            'grant_type': 'client_credentials',
            'client_id': current_app.config['KEYCLOAK_CLIENT_ID'],
            'client_secret': current_app.config['KEYCLOAK_CLIENT_SECRET']
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response, content = Http().request(
            uri=client_secrets['web']['token_uri'],
            method='POST',
            headers=headers,
            body=urlencode(body_dict)
        )

        if self._successful_response(response):
            service_token = json.loads(content.decode('utf-8'))
            return service_token['access_token']

        return None

    def get_user_by_id(self, user_id) -> Union[Dict[str, Any], None]:
        """Get realm user representation by id.

        Receive realm user representation from OP's view users endpoint GET
        request by specified [user_id] as url parameter.

        Returns:
            Union[Dict[str, Any], None]: User representation, None if response
            is unsuccessful.
        """
        uri = VIEW_USERS_URI.format(
            hostname=current_app.config['KEYCLOAK_ADDRESS'],
            port=current_app.config['KEYCLOAK_SERVER_PORT'],
            realm_name=current_app.config['KEYCLOAK_REALM_NAME'],
        ) + f'/{user_id}'

        response, content = Http().request(
            uri=uri,
            method='GET',
            headers=self.bearer_auth_header
        )

        if self._successful_response(response):
            user_representation = json.loads(content.decode('utf-8'))
            return user_representation

        return None

    def is_admin(self, user_id) -> bool:
        """Determines whether the user with specified [user_id] is an admin.

        Checks if user's role matches admin role specified in configuration.
        """
        user_role = self.get_client_role_by_id(user_id)
        return user_role == current_app.config['KEYCLOAK_ADMIN_ROLE']

    def _successful_response(self, response) -> bool:
        """Determines whether the response is successful.

        Args:
            response (Response): Any response object with status attribute.

        Returns:
            bool: True if response status is 2XX, False otherwise.
        """
        if hasattr(response, 'status'):
            if 200 <= response.status <= 299:
                return True
        return False


class Paginator:
    """Representation of paginated iterable object."""

    def __init__(self, items: Iterable, in_page: int, page=1) -> None:
        self.items = items
        self.in_page = in_page
        self.page = page
        self.pages: int = ceil(len(items) / in_page)
        self.has_prev: bool = self._has_prev()
        self.has_next: bool = self._has_next()

    def iter_pages(self) -> int:
        """Iterate over page numbers."""
        for page_num in range(1, self.pages + 1):
            yield page_num

    def get_page(self, num: int) -> Union[Iterable, None]:
        """Get page with specified number.

        Args:
            num (int): Number of the page.

        Returns:
            Union[Iterable, None]: Slice of given iterable object basing on
            numbers of items in the page, None if items does not exist.
        """
        if not self.items:
            return None

        start = (num - 1) * self.in_page
        end = num * self.in_page
        return self.items[start:end]

    def _has_prev(self) -> bool:
        """Determines whether the paginator's previous page exists."""
        if 1 < self.page <= self.pages:
            return True
        return False

    def _has_next(self) -> bool:
        """Determines whether the paginator's next page exists."""
        if self.page < self.pages:
            return True
        return False


class RealmUser:
    """Realm user object based on OP's user representation in dict type."""

    def __init__(self, user_representation: Dict[str, Any],
                 op_service_client=None) -> None:
        self.user_representation = user_representation
        try:
            self.id = self.user_representation['id']
            self.email = self.user_representation['email']
            self.firstname = self.user_representation['firstName']
            self.lastname = self.user_representation['lastName']
            self.fullname = self._get_fullname()
            self.op_service_client = op_service_client
            self.role = self._get_client_role()
        except Exception:
            current_app.logger.error(
                'Incomplete user representation. `%s` object creation failed!',
                self.__class__.__name__,
                exc_info=1
            )

    @property
    def get_email(self) -> str:
        return self.email

    @property
    def get_firstname(self) -> str:
        return self.firstname

    @property
    def get_lastname(self) -> str:
        return self.lastname

    def _get_fullname(self) -> str:
        return ' '.join([self.firstname, self.lastname])

    def _get_client_role(self) -> str:
        if self.op_service_client is None or \
                not isinstance(self.op_service_client, KeycloakServiceClient):
            return None

        return self.op_service_client.get_client_role_by_id(self.id)
