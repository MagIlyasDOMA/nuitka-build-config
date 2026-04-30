import sys, json

sys.argv.append('--nuitka-build-config-english-i18n-mode')

from nuitka_build_config.models import NuitkaConfig

with open('schema.json', 'w', encoding='utf-8') as file:
    schema = {'$schema': 'https://json-schema.org/draft-07/schema#'}
    schema.update(NuitkaConfig.model_json_schema())
    json.dump(schema, file, indent=2, ensure_ascii=False)
