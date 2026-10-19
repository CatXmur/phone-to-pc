[app]
title = PhoneToPC
package.name = phonetoppc
package.domain = org.bro.phonetoppc
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# ВАЖНО: Добавили hostpython3==3.11.9, чтобы версии Python на сервере и телефоне совпадали
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.1

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1