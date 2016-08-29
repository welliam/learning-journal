def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('list', '/')
    config.add_route('detail', '/journal/{id:\d+}')
    config.add_route('create', '/new-entry')
    config.add_route('update', '/journal/{id:\d+}/edit-entry')

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
