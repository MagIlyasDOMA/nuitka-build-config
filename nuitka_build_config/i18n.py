import locale, sys
from pathlib import Path
from typing import Callable
from locale_plus import Internationalizator
from ._english_i18n_mode import ENGLISH_I18N_MODE_ARG

locale.setlocale(locale.LC_ALL, '')


def create_gettext() -> Callable[[str], str]:
    lang = None
    if ENGLISH_I18N_MODE_ARG in sys.argv:
        lang = 'en_US'
        sys.argv.remove(ENGLISH_I18N_MODE_ARG)
    return Internationalizator(Path(__file__).parent / 'locale', lang, 'nbc').gettext


gettext = create_gettext()
