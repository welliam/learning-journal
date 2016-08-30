import os
import pytest
import transaction
from pyramid import testing

from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    EntryModel
)
from ..models.meta import Base


@pytest.fixture(scope="session")
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ["DATABASE_URL"]
    })
    config.include("..models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def testapp():
    from learning_journal import main
    from webtest import TestApp
    app = main({})
    return TestApp(app)


@pytest.fixture
def articles():
    return [{
        'title': 'one',
        'id': 1
    }, {
        'title': 'two',
        'id': 2
    }, {
        'title': 'three',
        'id': 3
    }]


def dummy_http_request(new_session):
    dummy = testing.DummyRequest()
    dummy.dbsession = new_session
    return dummy


@pytest.fixture
def request_with_model(new_session):
    new_session.add(EntryModel(title='title', body='body', date='August 1'))
    new_session.flush()
    return dummy_http_request(new_session)
