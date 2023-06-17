from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)
from .models import URLMap
from .settings import MAX_URL_LENGTH, SHORT_URL_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку', validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, MAX_URL_LENGTH),
            URL(require_tld=True, message=('Некорректный URL'))
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки', validators=[
            Length(1, SHORT_URL_LENGTH),
            Optional(),
            Regexp(
                r'^[A-Za-z0-9]+$',
                message='Можно использовать только [A-Z, a-z, 0-9]'
            )
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and URLMap.query.filter_by(short=field.data).first():
            raise ValidationError(f'Имя {field.data} уже занято!')