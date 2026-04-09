import locale
from pathlib import Path
from locale_plus import Internationalizator


locale.setlocale(locale.LC_ALL, '')

internationalizator = Internationalizator()

with open(mo_path, 'rb') as file:
    lang = i18n_lib.GNUTranslations(file)
gettext = lang.gettext
