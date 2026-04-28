<a id="doc_en"></a>
# Nuitka Build Config (nbc)
#### [Документация на русском](#doc_ru)

`nuitka-build-config` (nbc) is a tool for managing application builds with **Nuitka** using declarative configuration files (YAML/JSON). It provides a convenient Pydantic configuration model, a CLI for generation and building, as well as support for pre- and post-compilation actions.

## 📦 Features
- 🧩 **Declarative Configuration** — describe builds in YAML/JSON without writing commands.
- ⚙️ **Configuration Generation** — automatically create a configuration file from command line parameters.
- 🧠 **Pydantic Models** — strict validation and IDE autocompletion.
- 📦 **Plugin Support** — enable/disable Nuitka plugins.
- 🖥️ **Cross-platform** — separate parameters for Windows, macOS, Linux.
- 📋 **Pre/Post Compilation Actions** — run arbitrary commands (e.g., tests, packaging).
- 📊 **Report Generation** — create an XML compilation report.
- 🧹 **Build Directory Removal** — `--remove-output` option.

## 🚀 Installation

```bash
pip install nuitka-build-config
```

Or with `uv`:

```bash
uv add nuitka-build-config
```

After installation, the `nbc` command becomes available.

## 🧪 Usage
### 1. Generate a configuration file
```bash
nbc generate --main main.py --mode standalone --windows-console-mode disable -o myconfig.yaml
```

Almost all Nuitka parameters are supported (see `nbc generate --help`).

### 2. Build a project from a configuration file
```bash
nbc build myconfig.yaml
```

If `main` is not specified in the config, you can pass it as a second argument:

```bash
nbc build myconfig.yaml main.py
```

### 3. Generate build command without building (Dry-run)
```bash
nbc build --dry-run
```

This will show which Nuitka command would have been executed.

### 4. Example configuration (`nbc-config.yaml`)
```yaml
type: standalone
main: src/main.py
run: true
follow_stdlib: false
output_dir: ./dist
output_name: myapp
remove_output: true

include:
  packages:
    - requests
    - rich
  files:
    - ./assets/icon.png
    - [./data/, "data"]

plugins:
  - anti-bloat

windows_params:
  console_mode: disable
  uac_admin: true
  icon: ./assets/app.ico

python_flags:
  - -O           # remove asserts
  - no_warnings

pre_compile_actions:
  - echo "Starting build"

post_compile_actions:
  - upx --best dist/myapp.exe
```

## 🧱 Programmatic Usage
You can use the models inside your Python code:
```python
from nuitka_build_config.models import NuitkaConfig

config = NuitkaConfig.from_yaml_file("nbc-config.yaml")
print(config.output_dir)  # ./dist
```

## 🧰 CLI Commands

 | Command        | Description                    |
 |----------------|--------------------------------|
 | `nbc build`    | Run build from configuration   |
 | `nbc generate` | Generate config from arguments |
 | `nbc help`     | Help on commands               |

### Параметры `generate` (примеры)

| &nbsp;                           | &nbsp;                                       |
|----------------------------------|----------------------------------------------|
| `--mode onefile`                 | build mode                                   |
| `--enable-plugins tk-inter`      | enable plugin                                |
| `--windows-console-mode disable` | disable console                              |
| `-o config.yaml`                 | output file name (default `nbc-config.yaml`) |
| `--compile`                      | start build immediately after generation     |

## ⚙️ Requirements
- Python ≥ 3.9
- Nuitka ≥ 4.0
- Pydantic ≥ 2.0

## 🧩 Extensions and Customization
The package is designed to be modular. You can:
- Inherit from `NuitkaConfig` and add your own fields.
- Override `_add_*` methods in `DecoratorMixin`.
- Use `extra_flags` for any custom Nuitka arguments.

## 🌍 Internationalization
CLI messages and field descriptions support translations. Current languages:
**English**, **Русский**.

Translation files are located in `nuitka_build_config/locale/`.

## 📄 License
MIT License © MagIlyasDOMA

---

<a id="doc_ru"></a>
# Nuitka Build Config (nbc)
#### [Documentation in English](#doc_en)

`nuitka-build-config` (nbc) --- это инструмент для управления сборкой
приложений с помощью **Nuitka** через декларативные конфигурационные
файлы (YAML/JSON). Он предоставляет удобную Pydantic-модель
конфигурации, CLI для генерации и сборки, а также поддержку пред- и
пост-компиляционных действий.

## 📦 Возможности
- 🧩 **Декларативная конфигурация** --- описание сборки в YAML/JSON без
  написания команд.
- ⚙️ **Генерация конфигурации** --- автоматическое создание файла
  конфигурации из параметров командной строки.
- 🧠 **Pydantic-модели** --- строгая валидация и автодополнение в IDE.
- 📦 **Поддержка плагинов** --- включение/отключение плагинов Nuitka.
- 🖥️ **Кроссплатформенность** --- отдельные параметры для Windows,
  macOS, Linux.
- 📋 **Действия до/после компиляции** --- запуск произвольных команд
  (например, тесты, упаковка).
- 📊 **Генерация отчётов** --- создание XML-отчёта о компиляции.
- 🧹 **Удаление build-каталога** --- опция `--remove-output`.

## 🚀 Установка

```bash
pip install nuitka-build-config
```

Или с помощью `uv`:

```bash
uv add nuitka-build-config
```

После установки становится доступна команда `nbc`.

## 🧪 Использование

### 1. Генерация конфигурационного файла

```bash
nbc generate --main main.py --mode standalone --windows-console-mode disable -o myconfig.yaml
```

Поддерживаются почти все параметры Nuitka (см. `nbc generate --help`).

### 2. Сборка проекта по конфигурации
```bash
nbc build myconfig.yaml
```

Если `main` не указан в конфиге, его можно передать вторым аргументом:

```bash
nbc build myconfig.yaml main.py
```

### 3. Генерация команды сборки без сборки (Dry-run)

```bash
nbc build --dry-run
```

Покажет, какая команда Nuitka была бы выполнена.

### 4. Пример конфигурации (`nbc-config.yaml`)

```yaml
type: standalone
main: src/main.py
run: true
follow_stdlib: false
output_dir: ./dist
output_name: myapp
remove_output: true

include:
  packages:
    - requests
    - rich
  files:
    - ./assets/icon.png
    - [./data/, "data"]

plugins:
  - anti-bloat

windows_params:
  console_mode: disable
  uac_admin: true
  icon: ./assets/app.ico

python_flags:
  - -O           # удалить assert'ы
  - no_warnings

pre_compile_actions:
  - echo "Starting build"

post_compile_actions:
  - upx --best dist/myapp.exe
```

## 🧱 Программное использование

Вы можете использовать модели внутри своего Python-кода:

```python
from nuitka_build_config.models import NuitkaConfig

config = NuitkaConfig.from_yaml_file("config.yaml")
print(config.output_dir)  # ./dist
```

## 🧰 Команды CLI

 | Команда        | Описание                        |
 |----------------|---------------------------------|
 | `nbc build`    | Запуск сборки по конфигурации   |
 | `nbc generate` | Генерация конфига из аргументов |
 | `nbc help`     | Справка по командам             |

### Параметры `generate` (примеры)
| &nbsp;                           | &nbsp;                                            |
|----------------------------------|---------------------------------------------------|
| `--mode onefile`                 | режим сборки                                      |
| `--enable-plugins tk-inter`      | включить плагин                                   |
| `--windows-console-mode disable` | отключить консоль                                 |
| `-o config.yaml`                 | имя выходного файла (по умолч. `nbc-config.yaml`) |
| `--compile`                      | сразу после генерации запустить сборку            |

## ⚙️ Требования

- Python ≥ 3.9
- Nuitka ≥ 4.0
- Pydantic ≥ 2.0

## 🧩 Расширения и кастомизация

Пакет спроектирован модульно. Вы можете:

- Наследовать `NuitkaConfig` и добавлять свои поля.
- Переопределять методы `_add_*` в `DecoratorMixin`.
- Использовать `extra_flags` для любых кастомных аргументов Nuitka.

## 🌍 Интернационализация

Сообщения CLI и описания полей поддерживают переводы. Текущие языки:
**English**, **Русский**.

Файлы переводов находятся в `nuitka_build_config/locale/`.

## 📄 Лицензия
MIT License © MagIlyasDOMA
