import datetime
import sys

import random


DEFAULT_STRING_LENGTH = 8
DECIMAL_TEMPLATE = "%%d.%%0%dd"
EMAIL_TEMPLATE = "%s%%d@%s"
DATETIME_TEMPLATE = "%s %d:%d"
CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def loop(func):
    def loop_generator(*args, **kwargs):
        while 1:
            yield func(*args, **kwargs)
    return loop_generator


def sequence(func):
    def sequence_generator(*args, **kwargs):
        i = 0
        while 1:
            i += 1
            yield func(i, *args, **kwargs)
    return sequence_generator


def default_gen_maker(column):
    return loop(lambda: '')


def random_choice_iterator(choices=None, size=1):
    choices = choices or ['']
    for _ in xrange(0, size):
        yield random.choice(choices)


def random_string_maker(column, chars=None):
    " Generate String values. "

    max_length = getattr(column, 'length', DEFAULT_STRING_LENGTH)
    return loop(lambda: random_string(max_length, chars))


def random_string(max_length=None, chars=None):
    " Generate random string. "

    if max_length is None:
        max_length = DEFAULT_STRING_LENGTH
    if chars is None:
        chars = CHARS
    i = random_choice_iterator(chars, max_length)
    return ''.join(x for x in i)


def random_boolean_maker(column=None):
    " Generate random boolean. "

    return loop(lambda: random.choice((True, False)))


def random_null_boolean_maker(column=None):
    " Generate random boolean. "

    return loop(lambda: random.choice((None, True, False)))


def random_date_string():
    " Generate random date. "

    y = random.randint(1900, 2020)
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    return str(datetime.date(y, m, d))


def random_time_string():
    " Generate random time. "

    h = random.randint(0, 23)
    m = random.randint(0, 59)
    s = random.randint(0, 59)
    return str(datetime.time(h, m, s))


def random_date_string_maker(column):
    " Generate random date. "

    return loop(random_date_string)


def random_datetime_string():
    " Generate random datetime. "

    h = random.randint(1, 12)
    m = random.randint(0, 59)
    result = DATETIME_TEMPLATE % (random_date_string(), h, m)
    return result


def random_datetime_string_maker(column):
    " Generate random datetime. "

    return loop(random_datetime_string)


def random_decimal_maker(column):
    " Generate Numeric, DECIMAL types. "

    x = pow(10, column.precision - column.scale) - 1
    y = pow(10, column.scale) - 1
    fmt_string = DECIMAL_TEMPLATE % column.scale

    def gen():
        return fmt_string % (random.randint(1, x), random.randint(1, y))
    return loop(gen)


def email_generator(addr, domain):
    template = EMAIL_TEMPLATE % (addr, domain)

    def email_gen_maker(column):
        return sequence(lambda i: template % i)
    return email_gen_maker


def random_integer_maker(column, low=-2147483647, high=2147483647):
    if column.autoincrement:
        low = 1
    return loop(lambda: random.randint(low, high))


def random_big_integer_maker(column):
    return random_integer_maker(column, low=-9223372036854775808, high=9223372036854775807)


def random_small_integer_maker(column):
    return random_integer_maker(column, low=-32768, high=32767)


def random_small_positive_integer_maker(column):
    return random_integer_maker(column, low=0, high=32767)


def random_positive_integer_maker(column):
    return random_integer_maker(column, low=0)


def random_float_maker(column):
    return loop(random_float)


def random_auto_column_maker(column):
    return loop(lambda: random.randint(1, 2147483647))


def random_float():
    return random.uniform(sys.float_info.min, sys.float_info.max)


def random_ipaddress_maker(column):
    return loop(lambda: "%s.%s.%s.%s" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


def random_time_string_maker(column):
    return loop(random_time_string)
