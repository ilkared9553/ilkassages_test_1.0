[app]

# (str) Название приложения
title = ilkassages

# (str) Имя пакета (должно быть уникальным, в стиле reverse domain)
package.name = ilkassages_demo

# (str) Домен (часть идентификатора пакета)
package.domain = ilkassages.test

# (str) Путь к папке с исходным кодом (где лежит main.py)
source.dir = .

# (list) Расширения файлов, которые нужно включить в сборку
source.include_exts = py,png,jpg,kv,atlas,ttf,json

# (list) Паттерны для включения дополнительных файлов/папок (например, assets/)
# source.include_patterns = assets/*,images/*.png

# (list) Расширения файлов, которые нужно исключить
# source.exclude_exts = spec

# (list) Папки, которые нужно исключить из сборки
# source.exclude_dirs = tests, bin

# (list) Файлы, которые нужно исключить (по именам)
# source.exclude_patterns = license,readme/.*

# (str) Версия приложения (метод 1: из файла)
version = 0.1

# (str) Версия приложения (метод 2: строка)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Зависимости проекта
requirements = python3, kivy, kivymd, pillow, requests,

# (str) Ориентация экрана: all | landscape | portrait
orientation = portrait

# (list) Разрешения для Android (раскомментируйте нужные)
# android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# (int) Целевой API Android (рекомендуется 31 или выше)
android.api = 31

# (int) Минимальная версия API Android
android.minapi = 21

# (int) Версия NDK
android.ndk = 25b

# (str) Архитектура(и) для сборки (arm64-v8a, armeabi-v7a)
android.arch = arm64-v8a

# (bool) Автоматически принимать лицензии SDK
android.accept_sdk_license = True

# (str) Иконка приложения (путь относительно source.dir)
# icon.filename = %(source.dir)s/data/icon.png

# (str) Сплеш-скрин (заставка при запуске)
# splash.filename = %(source.dir)s/data/splash.png

# (str) Локализация: язык по умолчанию
osx.language = en

# (bool) Полноэкранный режим
fullscreen = 1

#
# Android specific
#

# (bool) Если True, то Buildozer будет скачивать Gradle автоматически
android.gradle_download = True

# (str) Дополнительно передаваемые аргументы для компиляции в Gradle
# android.gradle_extra_args =

# (bool) Включить AAB (Android App Bundle) вместо APK
# android.aab = False

# (str) Пароль для подписи APK (если не задан, будет создан временный)
# android.keystore.passwd = android

# (str) Путь к keystore файлу для подписи APK
# android.keystore.filename = release.keystore

# (str) Псевдоним ключа в keystore
# android.keystore.name = androiddebugkey

# (str) Пароль ключа (если не задан, совпадает с android.keystore.passwd)
# android.keyalias.passwd = android


#
# iOS specific
#

# (str) Path to Apple Developer Certificate
# ios.codesign.cert = entersign

# (str) Name of the code sign key
# ios.codesign.key = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) The development team identifier
# ios.codesign.team = <hexstring>

# (bool) Allow the compilation of non-free/closed source/proprietary dependencies
# ios.allow_dangerous_dependencies = False

# (bool) Set this to True if your app crashes because of PVRTC textures.
# ios.pvrtc_support = False


[buildozer]

# (int) Логирование: 0 = ошибки, 1 = предупреждения, 2 = информация, 3 = отладка
log_level = 2

# (bool) Запускать команду clean перед сборкой
# buildozer.clean = False

# (str) Директория для временных файлов сборки
# build_dir = ./.buildozer

# (str) Директория для финальных APK/IPA
# bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns as example:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    Instead of doing:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#


#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could first change the title to add "(demo)" in it, and
#    extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug

