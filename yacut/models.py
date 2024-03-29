from datetime import datetime
from random import sample
from re import match

from flask import url_for

from yacut import db
from .error_handlers import (OriginalTooLongError, ShortGeneratingError,
                             ShortIsTakenError, ShortSymbolsError,
                             ShortTooLongError)
from .settings import (MAX_URL_LENGTH, NUMBER_OF_CYCLES, REDIRECT_VIEW,
                       SHORT_LENGTH, SHORT_REG_EXP, USER_SHORT_LENGTH,
                       VALID_SYMBOLS)

INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
ORIGINAL_TOO_LONG = 'Оригинальная ссылка слишком длинная'
ID_IS_TAKEN = 'Имя "{id}" уже занято.'
SHORT_GENERATOR_ERROR = 'Не удалось сгенерировать короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW, short=self.short, _external=True
            ),
        )

    @staticmethod
    def create_entry(original, short, data_verified=False):
        if not data_verified:
            if len(original) > MAX_URL_LENGTH:
                raise OriginalTooLongError(ORIGINAL_TOO_LONG)
            if short:
                if len(short) > USER_SHORT_LENGTH:
                    raise ShortTooLongError(INVALID_SHORT_NAME)
                if not match(SHORT_REG_EXP, short):
                    raise ShortSymbolsError(INVALID_SHORT_NAME)
                if URLMap.get_entry(short=short):
                    raise ShortIsTakenError(ID_IS_TAKEN.format(id=short))
        if not short:
            short = URLMap.get_short()
        entry = URLMap(original=original, short=short)
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get_short():
        for _ in range(NUMBER_OF_CYCLES):
            short = ''.join(sample(VALID_SYMBOLS, SHORT_LENGTH))
            if not URLMap.get_entry(short=short):
                return short
        raise ShortGeneratingError(SHORT_GENERATOR_ERROR)

    @staticmethod
    def get_entry(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_original_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404().original
