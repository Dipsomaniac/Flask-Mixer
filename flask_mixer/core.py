from importlib import import_module

from sqlalchemy.orm.interfaces import MANYTOONE, ONETOMANY
from sqlalchemy.types import BIGINT, BOOLEAN, BigInteger, Boolean, CHAR, DATE, DATETIME, DECIMAL, Date, DateTime, FLOAT, Float, INT, INTEGER, Integer, NCHAR, NVARCHAR, NUMERIC, Numeric, SMALLINT, SmallInteger, String, TEXT, TIME, Text, Time, Unicode, UnicodeText, VARCHAR

from . import generators


class GeneratorRegistry:
    " Fabric of generators. "

    generators = dict()

    def __init__(self):
        self.add_generator([Boolean, BOOLEAN],
                           generators.random_boolean_maker)

        self.add_generator([String, VARCHAR, Unicode, NVARCHAR, NCHAR, CHAR],
                           generators.random_string_maker)

        self.add_generator([Date, DATE],
                           generators.random_date_string_maker)

        self.add_generator([DateTime, DATETIME],
                           generators.random_datetime_string_maker)

        self.add_generator([DECIMAL, Numeric, NUMERIC],
                           generators.random_decimal_maker)

        self.add_generator([Float, FLOAT],
                           generators.random_float_maker)

        self.add_generator([Integer, INTEGER, INT],
                           generators.random_integer_maker)

        self.add_generator([BigInteger, BIGINT],
                           generators.random_big_integer_maker)

        self.add_generator([SmallInteger, SMALLINT],
                           generators.random_small_integer_maker)

        self.add_generator([Text, UnicodeText, TEXT],
                           generators.random_string_maker)

        self.add_generator([Time, TIME],
                           generators.random_time_string_maker)

    def add_generator(self, types, func):
        for cls in types:
            self.generators[cls] = func

    def get(self, cls):
        return self.generators.get(
            cls,
            lambda f: generators.loop(lambda: ''))


class ModelMixer:
    " Generator for model. "

    generators = {}

    def __init__(self, model_class):
        if isinstance(model_class, basestring):
            mod, cls = model_class.rsplit('.', 1)
            mod = import_module(mod)
            model_class = getattr(mod, cls)
        self.model_class = model_class

    def blend(self, mixer, **explicit_values):
        target = self.model_class()

        model_explicit_values = {}
        related_explicit_values = {}
        for key, value in explicit_values.iteritems():
            if '__' in key:
                prefix, _, postfix = key.partition('__')
                params = related_explicit_values.setdefault(prefix, {})
                params[postfix] = value
            else:
                model_explicit_values[key] = value

        self.set_explicit_values(target, model_explicit_values)
        self.set_local_fields(
            target, mixer,
            exclude=model_explicit_values.keys(),
            related_explicit_values=related_explicit_values)
        return target

    @staticmethod
    def set_explicit_values(target, values):
        for k, v in values.iteritems():
            setattr(target, k, v)

    def set_local_fields(self, target, mixer, exclude=None, related_explicit_values=None):
        exclude = exclude or []
        related_explicit_values = related_explicit_values or dict()
        mapper = self.model_class._sa_class_manager.mapper
        columns = [c for c in mapper.columns if not c.
                   nullable and not c.name in exclude]
        for column in columns:
            if column.default:
                v = column.default.execute(mixer.db.session.bind)
            else:
                v = self.generator_for(mixer.registry, column).next()
            setattr(target, column.name, v)

        for prop in mapper.iterate_properties:
            if hasattr(prop, 'direction') and prop.direction == MANYTOONE:
                related_values = related_explicit_values.get(prop.key, dict())
                value = mixer.blend(prop.mapper.class_, **related_values)
                col = prop.local_remote_pairs[0][0]
                setattr(target, prop.key, value)
                setattr(target, col.name,
                        prop.mapper.identity_key_from_instance(value)[1][0])

    def generator_for(self, registry, column):
        cls = type(column.type)
        if not column.name in self.generators:
            gen_maker = registry.get(cls)
            generator = gen_maker(column)
            self.generators[column.name] = generator()
        return self.generators[column.name]
