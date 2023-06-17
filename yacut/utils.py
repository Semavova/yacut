from random import sample
from string import ascii_letters, digits

from .settings import SHORT_URL_LENGTH
from .models import URLMap


def get_unique_short_id():
    while True:
        short_id = ''.join(sample(ascii_letters + digits, SHORT_URL_LENGTH))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
