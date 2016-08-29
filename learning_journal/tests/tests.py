import pytest

from pyramid import testing

from ..models import EntryModel


TITLES = [
    'Day 8',
    'Day 9',
    'Day -3',
    'Day Foo',
    ''
]


INFO_KEYS = ['title', 'date', 'id']


WRAPPED_PATHS = [
    '/',
    '/journal/1',
    '/journal/2',
    '/journal/1/edit-entry',
    '/journal/2/edit-entry',
    '/new-entry'
]


def test_model_gets_added(new_session):
    """Test that a model gets added to the database."""
    assert len(new_session.query(EntryModel).all()) == 0
    model = EntryModel(title="a", body="b", date="never")
    new_session.add(model)
    new_session.flush()
    assert len(new_session.query(EntryModel).all()) == 1


def test_model_saves_title(new_session):
    """Test that a model's title gets saved correctly."""
    model = EntryModel(title="a", body="b", date="never")
    new_session.add(model)
    new_session.flush()
    assert new_session.query(EntryModel).one().title == 'a'


@pytest.mark.parametrize('titles', TITLES)
def test_model_saves_titles(new_session, titles):
    """Test that all titles are saved when added in sequence."""
    for title in titles:
        new_session.add(EntryModel(title=title, body="b", date="never"))
    new_session.flush()
    results = map(lambda e: e.title, new_session.query(EntryModel).all())
    assert set(titles) == set(results)


def test_list_view(request_with_model):
    """Test list view."""
    from ..views.default import list_view
    result = list_view(request_with_model)
    assert result['articles'][0].title == 'title'


@pytest.mark.parametrize('key', INFO_KEYS)
def test_detail_view_has_key(key, request_with_model):
    """Test detail view returns dict with INFO_KEYS."""
    from ..views.default import detail_view
    request_with_model.matchdict = {'id': 1}
    info = detail_view(request_with_model)
    assert hasattr(info['article'], key)


@pytest.mark.parametrize('key', INFO_KEYS)
def test_list_view_articles_have_key(key, request_with_model):
    """Test list view returns dict with INFO_KEYS."""
    from ..views.default import list_view
    info = list_view(request_with_model)
    assert all(map(lambda a: hasattr(a, key), info['articles']))
