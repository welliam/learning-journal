import os
from datetime import datetime
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from ..models import EntryModel

HERE = os.path.dirname(__file__)


def get_article_by_id(dbsession, id):
    query = dbsession.query(EntryModel)
    return query.filter(EntryModel.id == id).first()


@view_config(route_name='list', renderer="templates/list.jinja2")
def list_view(request):
    return {
        'articles': request.dbsession.query(EntryModel).all()
    }


@view_config(route_name='detail', renderer="templates/detail.jinja2")
@view_config(route_name='update', renderer="templates/update.jinja2")
def detail_view(request):
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


@view_config(route_name='create', renderer="templates/new.jinja2")
def new_view(request):
    if request.method == "POST":
        request.dbsession.add(EntryModel(
            title=request.POST['title'],
            date=datetime.now().strftime('%B %w'),
            body=request.POST['body']
        ))
        return HTTPFound(location='/')
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
