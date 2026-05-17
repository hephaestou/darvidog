[app]
title = Darvidog Soil Analyser
package.name = darvidog
package.domain = com.gaiandynamics
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,wav
version = 1.0
requirements = python3,kivy==2.3.1,plyer
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FLASHLIGHT
orientation = portrait
icon.filename = %(source.dir)s/icon_corrected.png
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
