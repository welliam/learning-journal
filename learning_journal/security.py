import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import Everyone, Authenticated, Allow

from passlib.apps import custom_app_context as pwd_context


class Root(object):
    """Root object for this project."""
    def __init__(self, request):
        """Initialize a new Root."""
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'secret')
    ]


def check_credentials(user, password):
    """Check that user and password match environment variables."""
    correct_user = os.environ.get('LEARNING_JOURNAL_USERNAME', '')
    correct_password = os.environ.get('LEARNING_JOURNAL_PASSWORD', '')
    if correct_user and correct_password and user == correct_user:
        try:
            return pwd_context.verify(password, correct_password)
        except ValueError:
            pass
    return False


def set_session_factory(config):
    session_secret = os.environ.get('SESSION_SECRET', '~seeecret~')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)


def includeme(config):
    """Security-related configs."""
    auth_secret = os.environ.get('AUTH_SECRET', '~secret~')
    config.set_authentication_policy(AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    ))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_default_permission('view')
    config.set_root_factory(Root)
    set_session_factory(config)
    config.set_default_csrf_options(require_csrf=True)
