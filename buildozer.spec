[app]

# (str) Title of your application
title = GpsRotam

# (str) Package name
package.name = gpsrotam

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt,json

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# Hata tespiti için sadece temel kütüphaneleri bıraktık. Başarılı olunca KivyMD vb. ekleyeceğiz.
requirements = python3,kivy

# (str) Uygulamanın ana dosyasının adı 'ana.py' olduğu için bu satır gereklidir.
main.filename = ana.py 

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# Konum (GPS) ve İnternet izni eklendi.
android.permissions = android.permission.INTERNET, android.permission.ACCESS_FINE_LOCATION, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
# API Lisans sorununu çözmek için 28'de kalıyor.
android.api = 30

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
# Logların istediği minimum NDK sürümünü (25) ayarlıyoruz.
android.ndk = 25b

# (int) Android NDK API to use. Bu satırın eksikliği/hatası vardı, düzelttik.
android.ndk_api = 24

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
