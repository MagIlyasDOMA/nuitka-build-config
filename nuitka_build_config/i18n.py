import gettext as i18n_lib, locale
from pathlib import Path


locale.setlocale(locale.LC_ALL, '')

mo_path = Path(__file__).parent / 'locale' / (locale.getlocale()[0] or 'en_US') / 'nbc.mo'

with open(mo_path, 'rb') as file:
    lang = i18n_lib.GNUTranslations(file)
gettext = lang.gettext
