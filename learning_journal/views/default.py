import os
from datetime import datetime

from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from ..models import EntryModel
from ..security import check_credentials


HERE = os.path.dirname(__file__)


def get_article_by_id(dbsession, id):
    """From a database session and id, get the corresponding entry."""
    query = dbsession.query(EntryModel)
    return query.filter(EntryModel.id == id).first()


@view_config(route_name='list', renderer="templates/list.jinja2")
def list_view(request):
    """Return context for view for the home page."""
    return {
        'articles': request.dbsession.query(EntryModel).all()
    }


@view_config(
    route_name='update',
    renderer="templates/update.jinja2",
    permission='secret'
)
@view_config(route_name='detail', renderer="templates/detail.jinja2")
def detail_view(request):
    """Return context for viewing an individual entry."""
    if request.method == "POST":
        article = {
            'title': request.POST['title'],
            'date': request.POST['date'],
            'body': request.POST['body'],
            'id': request.matchdict['id']
        }
    else:
        article = get_article_by_id(
            request.dbsession,
            int(request.matchdict['id'])
        )
    return {'article': article}


@view_config(
    route_name='create',
    renderer="templates/new.jinja2",
    permission='secret'
)
def new_view(request):
    """Return context for new entries.

    Redirects to root if POSTing a new entry."""
    if request.method == "POST":
        request.dbsession.add(EntryModel(
            title=request.POST['title'],
            date=datetime.now().strftime('%B %w'),
            body=request.POST['body']
        ))
        return HTTPFound(location='/')
    return {}


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    """Return context for login view."""
    if request.authenticated_userid:
        return HTTPFound(location='/')  # already logged in, redirect to /
    if request.method == "POST":
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(username, password):
            return HTTPFound(location='/', headers=remember(request, username))
    return {}


@view_config(
    route_name='logout',
    renderer='templates/logout.jinja2',
    permission='secret'
)
def logout_view(request):
    """Return context for login view."""
    return HTTPFound(location='/', headers=forget(request))
