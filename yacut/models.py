from datetime import datetime
from random import sample

from flask import url_for

from yacut import db

from .settings import (MAX_URL_LENGTH, NUMBER_OF_CYCLES, REDIRECT_VIEW,
                       SHORT_URL_LENGTH, VALID_SYMBOLS)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_URL_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_VIEW, short=self.short, _external=True
            ),
        )

    @staticmethod
    def create_entry(original, short):
        if short is None:
            short = URLMap.get_short_id()
        else:
            short = short
        db.session.add(URLMap(original=original, short=short))
        db.session.commit()
        return short

    @staticmethod
    def get_short_id():
        for _ in range(NUMBER_OF_CYCLES):
            short_id = ''.join(sample(VALID_SYMBOLS, SHORT_URL_LENGTH))
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id

    @staticmethod
    def get_entry(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_original_link(short):
        return URLMap.query.filter_by(short=short).first_or_404().original
