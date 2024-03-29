from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db


class ShortGeneratingError(Exception):
    """Вызывается при проблемах с генерированием короткой ссылки"""
    pass


class OriginalTooLongError(Exception):
    """Вызывается при превышении длины оригинальной ссылки"""
    pass


class ShortTooLongError(Exception):
    """Вызывается при превышении длины короткой ссылки"""
    pass


class ShortSymbolsError(Exception):
    """Вызывается если короткая ссылка содержит запрещенные символы"""
    pass


class ShortIsTakenError(Exception):
    """Вызывается если короткая ссылка уже занята"""
    pass


class InvalidAPIUsageError(Exception):

    def __init__(self, message, status_code=HTTPStatus.BAD_REQUEST):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), HTTPStatus.INTERNAL_SERVER_ERROR


@app.errorhandler(InvalidAPIUsageError)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code
