import pytest
import transaction

from pyramid import testing

from ..models import (
    EntryModel,
    get_engine,
    get_session_factory,
    get_tm_session,
)
from ..models.meta import Base

TITLES = [
    'Day 8',
    'Day 9',
    'Day -3',
    'Day Foo'
]


@pytest.fixture(scope="session")
def sqlengine(request):
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
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


def test_model_gets_added(new_session):
    assert len(new_session.query(EntryModel).all()) == 0
    model = EntryModel(title="a", body="b", date="never")
    new_session.add(model)
    new_session.flush()
    assert len(new_session.query(EntryModel).all()) == 1


def test_model_saves_title(new_session):
    assert len(new_session.query(EntryModel).all()) == 0
    model = EntryModel(title="a", body="b", date="never")
    new_session.add(model)
    new_session.flush()
    assert new_session.query(EntryModel).one().title == 'a'


@pytest.mark.parametrize('titles', TITLES)
def test_model_saves_titles(new_session, titles):
    for title in titles:
        new_session.add(EntryModel(title=title, body="b", date="never"))
    new_session.flush()
    results = map(lambda e: e.title, new_session.query(EntryModel).all())
    assert set(titles) == set(results)


# def dummy_http_request(new_session):
#     return testing.DummyRequest()
#
#
# def test_my_view(new_session):
#     from ..views.default import my_view
#
#     new_session.add(EntryModel(name="one", value=1))
#     new_session.flush()
#
#     http_request = dummy_request(new_session)
#     result = my_view(http_request)
#     assert result["one"].name == "one"
