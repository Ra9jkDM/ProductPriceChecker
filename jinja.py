from database import role

def setup(app, prefix=''):
    app.jinja_env.globals['PREFIX'] = prefix
    app.jinja_env.filters["is_admin"] = role.is_admin