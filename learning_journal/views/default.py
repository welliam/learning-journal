import os
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from sqlalchemy.exc import DBAPIError
from ..models import Entry
from .articles import articles

HERE = os.path.dirname(__file__)


def get_article_by_id(articles, id):
    try:
        return [article for article in articles if article['id'] == int(id)][0]
    except IndexError:
        raise HTTPNotFound('Article id not found: ' + id)


@view_config(route_name='list', renderer="templates/list.jinja2")
def list_view(request):
    request.dbsession.query(Entry).all()
    return {
        'articles': articles
    }


@view_config(route_name='detail', renderer="templates/detail.jinja2")
def detail_view(request):
    return get_article_by_id(articles, request.matchdict['id'])


@view_config(route_name='create', renderer="templates/new.jinja2")
def new_view(request):
    return {}


@view_config(route_name='update', renderer="templates/update.jinja2")
def update_view(request):
    return get_article_by_id(articles, request.matchdict['id'])


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(MyModel)
#         one = query.filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'learning_journal'}


# @view_config(route_name="edit", renderer="../templates/edit-model.jinja2")
# def edit_view(request):
#     return {"data": {"name": "A new form"}}


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
