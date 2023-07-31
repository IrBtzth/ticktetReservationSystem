import os
from webapp import db, migrate, create_app
from webapp.app.models import Routes

from flask_migrate import Migrate

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())

#app.app_context().push()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Routes=Routes,
                    migrate=migrate)