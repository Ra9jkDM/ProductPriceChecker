from views import view, files, users, api, proxy


def register_blueprints(app):
    app.register_blueprint(view.view)
    app.register_blueprint(users.users)

    app.register_blueprint(files.file)
    app.register_blueprint(api.api, url_prefix="/api")
    app.register_blueprint(proxy.proxy, url_prefix="/proxy")
