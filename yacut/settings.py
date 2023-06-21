from re import escape
from string import ascii_letters, digits

VALID_SYMBOLS = ascii_letters + digits
SHORT_REG_EXP = rf'^[{escape(VALID_SYMBOLS)}]+$'
SHORT_LENGTH = 6
USER_SHORT_LENGTH = 16
MAX_URL_LENGTH = 2048
NUMBER_OF_CYCLES = 10
REDIRECT_VIEW = 'redirect_view'
