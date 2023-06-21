from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (URL, DataRequired, Length, Optional, Regexp,
                                ValidationError)

from .models import URLMap
from .settings import MAX_URL_LENGTH, REG_EXP, USER_SHORT_LENGTH, VALID_SYMBOLS

ENTER_URL = 'Введите ссылку'
REQUIRED_FIELD = 'Обязательное поле'
INVALID_URL = 'Некорректный URL'
ENTER_SHORT = 'Ваш вариант короткой ссылки'
ALLOWED_SYMBOLS = 'Можно использовать только {symbols}'
CREATE = 'Создать'
ID_IS_TAKEN = 'Имя {id} уже занято!'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ENTER_URL, validators=[
            DataRequired(message=REQUIRED_FIELD),
            Length(max=MAX_URL_LENGTH),
            URL(require_tld=True, message=INVALID_URL)
        ]
    )
    custom_id = StringField(
        ENTER_SHORT, validators=[
            Length(max=USER_SHORT_LENGTH),
            Optional(),
            Regexp(
                REG_EXP,
                message=ALLOWED_SYMBOLS.format(symbols=VALID_SYMBOLS)
            )
        ]
    )
    submit = SubmitField(CREATE)

    def validate_custom_id(self, field):
        if field.data and URLMap.get_entry(short=field.data):
            raise ValidationError(ID_IS_TAKEN.format(id=field.data))
