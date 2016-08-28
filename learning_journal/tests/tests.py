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
    from ..views.default import list_view
    result = list_view(request_with_model)
    assert result['articles'][0].title == 'title'


@pytest.mark.parametrize('key', INFO_KEYS)
def test_detail_view_has_key(key, request_with_model):
    from ..views.default import detail_view
    request_with_model.matchdict = {'id': 1}
    info = detail_view(request_with_model)
    assert hasattr(info['article'], key)


@pytest.mark.parametrize('key', INFO_KEYS)
def test_list_view_articles_have_key(key, request_with_model):
    from ..views.default import list_view
    info = list_view(request_with_model)
    assert all(map(lambda a: hasattr(a, key), info['articles']))


# # wrapper


# @pytest.mark.parametrize('path', WRAPPED_PATHS)
# def test_layout_root_title(testapp, path):
#     response = testapp.get(path, status=200)
#     assert b'Learning Journal' in response.body


# @pytest.mark.parametrize('path', WRAPPED_PATHS)
# def test_layout_root_css(testapp, path):
#     response = testapp.get(path, status=200)
#     assert b'/static/style.css' in response.body


# @pytest.mark.parametrize('path', WRAPPED_PATHS)
# def test_layout_root_doctype(testapp, path):
#     response = testapp.get(path, status=200)
#     assert b'<!DOCTYPE html>' in response.body


# # list


# def test_layout_list_about_section(testapp):
#     response = testapp.get('/', status=200)
#     assert b'<section id="about">' in response.body


# def test_layout_list_sections(testapp):
#     response = testapp.get('/', status=200)
#     assert b'<section id="entries">' in response.body


# def test_layout_list_new_link(testapp):
#     response = testapp.get('/', status=200)
#     assert b'href="new-entry"' in response.body


# # detail


# def test_layout_detail_article(testapp):
#     response = testapp.get('/journal/1', status=200)
#     assert b'</article>' in response.body


# def test_layout_detail_posted_on(testapp):
#     response = testapp.get('/journal/1', status=200)
#     assert b'Posted on' in response.body


# def test_layout_detail_edit_link(testapp):
#     response = testapp.get('/journal/1', status=200)
#     assert b'/edit-entry' in response.body


# def test_layout_detail_new_link(testapp):
#     response = testapp.get('/journal/1', status=200)
#     assert b'href="/new-entry"' in response.body


# # new


# def test_layout_new_form(testapp):
#     response = testapp.get('/journal/1/edit-entry', status=200)
#     assert b'</form>' in response.body


# def test_layout_new_inputs(testapp):
#     response = testapp.get('/journal/1/edit-entry', status=200)
#     assert b'input' in response.body


# def test_layout_new_method_post(testapp):
#     response = testapp.get('/journal/1/edit-entry', status=200)
#     assert b'method="POST"' in response.body


# # update


# def test_layout_update_form(testapp):
#     response = testapp.get('/journal/1/edit-entry', status=200)
#     assert b'</form>' in response.body


# def test_layout_update_inputs(testapp):
#     response = testapp.get('/journal/1/edit-entry', status=200)
#     assert b'input' in response.body


# def test_layout_update_method_post(testapp):
#     response = testapp.get('/journal/1/edit-entry', status=200)
#     assert b'method="POST"' in response.body
