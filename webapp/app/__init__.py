def create_module(app, **kwargs):
    from .controllers import app_blueprint
    app.register_blueprint(app_blueprint)
