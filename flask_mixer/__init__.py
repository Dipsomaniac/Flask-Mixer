__version__ = '0.1.5'
__project__ = __name__
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "GNU LGPL"


class Mixer:
    " Base container for models and generators. "

    def __init__(self, app, registry=None, session_add=True, session_commit=False):
        " Initialize mixer, registry and models. "

        from .core import GeneratorRegistry, RANDOM

        self.models = dict()
        self.random = RANDOM
        self.session_add = session_add
        self.session_commit = session_commit
        self.registry = registry or GeneratorRegistry()
        self.app = app
        self.db = None
        if self.app:
            self.init_app(app)

    def init_app(self, app):
        " Get db from application. "

        self.app = app
        assert app.extensions and app.extensions[
            'sqlalchemy'], "Flask-SQLAlchemy must be inialized before Mixer."
        self.db = app.extensions['sqlalchemy'].db
        self.app.extensions['milkman'] = self

    def blend(self, tablename, **values):
        " Generate instance of model. "

        from .core import ModelMixer

        model_mixer = self.models.setdefault(tablename, ModelMixer(tablename))
        result = model_mixer.blend(self, **values)

        if self.session_add:
            self.db.session.add(result)

        if self.session_commit:
            self.db.session.commit()

        return result
