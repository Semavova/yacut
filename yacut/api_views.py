from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .models import URLMap
from .settings import USER_SHORT_URL_LENGTH, VALID_SYMBOLS

REQUEST_BODY_IS_MISSING = 'Отсутствует тело запроса'
URL_IS_MISSING = '"url" является обязательным полем!'
INVALID_SHORT_URL_NAME = 'Указано недопустимое имя для короткой ссылки'
ID_IS_TAKEN = 'Имя "{id}" уже занято.'
ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsageError(REQUEST_BODY_IS_MISSING)
    if 'url' not in data:
        raise InvalidAPIUsageError(URL_IS_MISSING)
    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = URLMap.get_short_id()
    for symbol in data['custom_id']:
        if symbol not in VALID_SYMBOLS:
            raise InvalidAPIUsageError(
                INVALID_SHORT_URL_NAME
            )
    if len(data['custom_id']) > USER_SHORT_URL_LENGTH:
        raise InvalidAPIUsageError(
            INVALID_SHORT_URL_NAME
        )
    if URLMap.get_entry(short=data['custom_id']):
        raise InvalidAPIUsageError(ID_IS_TAKEN.format(id=data['custom_id']))
    URLMap.create_entry(original=data['url'], short=data['custom_id'])
    return jsonify(
        URLMap.get_entry(short=data['custom_id']).to_dict()
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_url(short_id):
    url_map = URLMap.get_entry(short=short_id)
    if not url_map:
        raise InvalidAPIUsageError(
            ID_NOT_FOUND, HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original})
