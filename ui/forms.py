from wtforms import Form, IntegerField, SelectMultipleField
from data_reader.data import get_symbols

symbols = get_symbols()


class StartForm(Form):
    balance = IntegerField('Balance')
    coins = SelectMultipleField('Coins', choices=[(s, s) for s in symbols])
