from flask import (
    current_app, render_template, make_response, Blueprint, request, url_for
)

from flask_admin import AdminIndexView
from werkzeug.utils import redirect

from tracker.blueprints.user.models import KeycloakServiceClient, CurrentUser
from tracker.extensions import openid_connect
from urllib.parse import quote

tracker_admin = Blueprint('tracker_admin', __name__, template_folder='templates')


class CustomAdminIndexView(AdminIndexView):

    def is_accessible(self):
        return CurrentUser().is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('page.home'))


@tracker_admin.route('/admin_query/<int:pk>/')
@openid_connect.require_login
def admin_query(pk):
    context = {
        'name': "unknown",
        'pk': pk,
        'data': [],
        'keys': [],
        'keycloak': KeycloakServiceClient
    }
    return render_template(
        'tracker_admin/admin-query.html',
        **context,
    )


@tracker_admin.route('/admin_query/<int:pk>/csv')
@openid_connect.require_login
def admin_query_csv(pk):
    headings, rows, query_name = [], [], "unknown"
    csv_content = ",".join(headings)
    rows = [[str(value) for (key, value) in o.items()] for o in rows]
    rows = [','.join(row) for row in rows]
    csv_content += "\n" + "\n".join(rows)
    response = make_response(csv_content)
    response.headers['Content-Disposition'] = f'attachment; filename={quote(query_name, encoding="utf-8")}-dump.csv'
    response.headers['Content-Encoding'] = 'utf-8'
    response.mimetype = 'text/csv'
    return response


@tracker_admin.route('/statistics/')
@openid_connect.require_login
def admin_query_list_statistic():
    aqs = []

    context = {
        'data': aqs,
        'title': 'Statistics',
        'keycloak': KeycloakServiceClient
    }

    return render_template(
        'tracker_admin/admin-query-list.html',
        **context
    )


@tracker_admin.route('/diagnostics/')
@openid_connect.require_login
def admin_query_list_diagnostic():
    aqs = []

    context = {
        'data': aqs,
        'title': 'Diagnostics',
        'keycloak': KeycloakServiceClient
    }

    return render_template(
        'tracker_admin/admin-query-list.html',
        **context,
    )
