import datetime
import json
import string
import random
import time

import pytz

from config import Config

from flask import request


def pics_to_array(product):
    product.images = product.images.split(',')


def dict_pic_to_list(product):
    product['images'] = product['images'].split(',')


def generate_sku():
    return "".join([random.choice(string.digits) for _ in range(3)]) + "-" + "".join(
        [random.choice(string.ascii_uppercase) for _ in range(3)]) + "-" + "".join(
        [random.choice(string.digits) for i in range(3)])


def get_ip():
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return ip


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_time(readable=False):
    if readable:
        r = time.ctime()
        return r
    millis = int(round(time.time() * 1000))
    return millis


def number_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def group_int(number):
    number = float(number)
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))


def future_milliseconds_datetime(f_date: int, d_date=None):
    if d_date is None:
        f = datetime.datetime.now() + datetime.timedelta(days=f_date)
    else:
        f = datetime.datetime.strptime(
            d_date, '%Y-%m-%d') + datetime.timedelta(days=f_date)

    timestamp = f.timestamp()
    return int(round(timestamp) * 1000)


def future_milliseconds_hour(hours):
    f = datetime.datetime.now() + datetime.timedelta(hours=hours)
    return int(round(f.timestamp()) * 1000)


def same_milliseconds_dates(timestamp1, timestamp2):
    # Create timezone-aware datetime objects
    tz = pytz.timezone('Africa/Lagos')  # Use the appropriate time zone
    date1 = datetime.datetime.fromtimestamp(timestamp1 / 1000, tz)
    date2 = datetime.datetime.fromtimestamp(timestamp2 / 1000, tz)

    # Compare year, month, and day components
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day


def hooks_log(data: dict, fn):
    file = Config.HOOKS_LOGS_DIR + '/' + fn + '.json'
    with open(file, 'w') as j:
        j.write(json.dumps(data))
