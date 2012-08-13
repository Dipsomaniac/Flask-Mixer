__version__ = version = '0.1.0'
__project__ = project = __name__
__author__ = author = "Kirill Klenov <horneds@gmail.com>"
__license__ = license = "GNU LGPL"


class Mixer:
    " Base container for models and generators. "

    def __init__(self, app, registry=None, session_add=True, session_commit=False):
        " Initialize mixer, registry and models. "

        from .core import GeneratorRegistry

        self.models = dict()
        self.session_add = session_add
        self.session_commit = session_commit
        self.registry = registry or GeneratorRegistry()
        self.app = app
        if self.app:
            self.init_app(app)

    def init_app(self, app):
        " Get db from application. "

        self.app = app
        assert app.extensions and app.extensions['sqlalchemy'], "Flask-SQLAlchemy must be inialized before Mixer."
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
            self.db.session.commit(result)

        return result
