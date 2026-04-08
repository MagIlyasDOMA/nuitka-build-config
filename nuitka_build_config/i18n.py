import gettext as i18n_lib, locale

locale.setlocale(locale.LC_ALL, '')

lang = i18n_lib.translation('nbc', 'locale', [locale.getlocale()[0]])

gettext = lang.gettext
