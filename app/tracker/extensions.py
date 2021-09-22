from flask_debugtoolbar import DebugToolbarExtension
from flask_oidc import OpenIDConnect
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

debug_toolbar = DebugToolbarExtension()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
openid_connect = OpenIDConnect()
