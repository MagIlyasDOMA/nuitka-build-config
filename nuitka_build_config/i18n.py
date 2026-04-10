import locale
from pathlib import Path
from locale_plus import Internationalizator


locale.setlocale(locale.LC_ALL, '')

gettext = Internationalizator(Path(__file__).parent / 'locale', domain='nbc').gettext
