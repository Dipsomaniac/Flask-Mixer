# -*- coding: utf-8 -*-
"""
    Flask-Mixer
    ===========

    Flask-Mixer is an extension for `Flask`_ that adds object generation
    tool for testing your application.

"""

__version__ = '0.1.8'
__project__ = __name__
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "GNU LGPL"


class Mixer:
    """This class is used for integration to one or more Flask
    applications.

    :param app: Flask application
    :param registry: Generators fabric :class:`GeneratorRegistry`
    :param session_add: Auto append generated instance to session
    :param session_commit: Auto commit db.session

    ::

        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db = SQLAlchemy()
        db.init_app(app)

        mixer = Mixer(app, session_commit=True)
        ...
        user = mixer.blend('app.models.User')

    The second possibility is to create the object once and configure the
    application later to support it::

        mixer = Mixer()
        ...
        mixer.init_app(app)


    """

    def __init__(self, app=None, registry=None, session_add=True, session_commit=False):
        """Initialize Mixer.
        """
        from .core import GeneratorRegistry, RANDOM

        self.models = dict()
        self.random = RANDOM
        self.session_add = session_add or session_commit
        self.session_commit = session_commit
        self.registry = registry or GeneratorRegistry()
        self.db = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        """This callback can be used to initialize an application for the
        use with this mixer setup.

        :param app: Flask application
        """
        assert app.extensions and app.extensions[
            'sqlalchemy'], "Flask-SQLAlchemy must be inialized before Mixer."
        self.db = app.extensions['sqlalchemy'].db

        # register extension with app
        app.extensions['mixer'] = self

    def blend(self, tablename, **values):
        """Generate instance of model.

        :param tablename: ModelClass or string with import path
        :param values: values for generate instance
        """

        from .core import ModelMixer

        model_mixer = self.models.setdefault(tablename, ModelMixer(tablename))
        result = model_mixer.blend(self, **values)

        if self.session_add:
            self.db.session.add(result)

        if self.session_commit:
            self.db.session.commit()

        return result
