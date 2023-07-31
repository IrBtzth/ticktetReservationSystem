def create_module(app, **kwargs):
    from .controllers import repositories_blueprint

    app.register_blueprint(repositories_blueprint)