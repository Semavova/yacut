from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .models import URLMap

REQUEST_BODY_IS_MISSING = 'Отсутствует тело запроса'
URL_IS_MISSING = '"url" является обязательным полем!'
ID_NOT_FOUND = 'Указанный id не найден'
ERROR = 'Произошла ошибка при создании короткой ссылки'


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsageError(REQUEST_BODY_IS_MISSING)
    if 'url' not in data:
        raise InvalidAPIUsageError(URL_IS_MISSING)
    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = None
    try:
        return jsonify(
            URLMap.create_entry(
                original=data['url'], short=data['custom_id']
            ).to_dict()
        ), HTTPStatus.CREATED
    except Exception:
        raise InvalidAPIUsageError(ERROR)


@app.route('/api/id/<string:short_id>/')
def get_url(short_id):
    url_map = URLMap.get_entry(short=short_id)
    if not url_map:
        raise InvalidAPIUsageError(
            ID_NOT_FOUND, HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': url_map.original})
