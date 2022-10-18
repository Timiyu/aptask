# coding=utf8
from datetime import datetime
import re

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
            1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']}

def intcomma(value):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    orig = str(value)
    new = re.sub(r"^(-?\d+)(\d{3})", r'\g<1>, \g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new)

def approximate_size(size, a_kilobyte_is_1024_bytes=True):
    '''Convert a file size to human-readable form.

    Keyword arguments:
    size -- file size in bytes
    a_kilobyte_is_1024_bytes -- if True (default), use multiples of 1024
                                if False, use multiples of 1000

    Returns: string

    '''
    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if a_kilobyte_is_1024_bytes else 1000
    for suffix in SUFFIXES[multiple]:
        size /= multiple
        if size < multiple:
            return '{0:.1f} {1}'.format(size, suffix)

    raise ValueError('number too large')


def timeConvert(size):  # 单位换算
    import math
    xs = size - math.floor(size)
    zs = size - xs
    size = zs
    M, H = 60, 60 ** 2
    if size < M:
        return str(int(zs)) + u'秒'
    if size < H:
        return u'%s分钟%s秒' % (int(size / M), int(size % M))
    else:
        hour = int(size / H)
        mine = int(size % H / M)
        second = int(size % H % M)
        tim_srt = u'%s小时%s分钟%s秒' % (hour, mine, second)
        return tim_srt


def chinese_time(x):
    if x is None:
        y = ''
    else:
        y = datetime.strftime(x, '%Y{y}%m{m}%d{d} %H{hour}%M{min}%S{sec}').format \
            (y='年', m='月', d='日', hour='时', min='分', sec='秒')
    return y


# 用于转换tags
# 逗号分隔字符串转list
def str_list(list_str):
    if list_str == '':
        resp_list = ''
    else:
        list_str = list_str.split(",")
        resp_list = []
        for item in list_str:
            item = item.replace(' ', '')
            item = item.replace("'", '')
            resp_list.append(item)
        resp_list[0] = resp_list[0].replace('[', '')
        resp_list[-1] = resp_list[-1].replace(']', '')
    return resp_list


# list转逗号分隔字符串
def list_str(str_list):
    if len(str_list) == 0:
        resp_str = ''
    else:
        resp_str = ','.join(str_list)
    return resp_str
