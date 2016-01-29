import random
import string
import datetime


def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generates an ID of characters with standard size 6

    :param size: size of id
    :param chars: which characters should be uses
    :return:
    :rtype: str
    """
    return ''.join(random.choice(chars) for _ in range(size))


def generate_datetime(string_format="%Y-%m-%d %H:%M:%S", date=None):
    """

    :param string_format:
    :param date:
    :return:
    :rtype: datetime.datetime
    """
    gen_now(string_format, date, date_return=True)


def generate_datestring(string_format="%Y-%m-%d %H:%M:%S", date=None):
    """

    :param string_format:
    :param date:
    :return:
    :rtype: datetime.datestring
    """
    gen_now(string_format, date, date_return=False)


def gen_now(string_format="%Y-%m-%d %H:%M:%S", date=None, date_return=False):
    """
    Liefert ein Datum als Antwort als String im Format 'sf'.
    Bei DATE_RETURN=True wird als Ergebnis ein Typ datetime.datetime als Antwort gegeben.

    :type string_format: str
    :param string_format: date format %Y,%m, ...
    :type date_return: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :param date_return: if set True return changes from string to datetime.datetime

    :rtype: str, datetime.datetime
    :return: datetime as string or type
    """
    if date is None:
        date = datetime.datetime.now().strftime(string_format)

    if date_return:
        return datetime.datetime.strptime(date, string_format)
    else:
        return date