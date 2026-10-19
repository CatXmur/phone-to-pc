[app]
title = Phone To PC
package.name = phonetoppc
package.domain = org.bro.phonetoppc

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy

# ВАЖНО: разрешение на интернет для Android
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk_api = 21
android.accept_sdk_license = True

orientation = portrait
fullscreen = 0