[app]
title = Darvidog Soil Analyser
package.name = darvidog
package.domain = com.gaiandynamics

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,wav

version = 1.0

requirements = python3==3.11.11,kivy==2.3.0,kivymd==1.2.0,plyer

android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FLASHLIGHT
android.features = android.hardware.camera

orientation = portrait

icon.filename = %(source.dir)s/icon_corrected.png

android.api = 33
android.minapi = 24
android.ndk = 25b
android.build_tools_version = 34.0.0
android.accept_sdk_license = True
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk

[buildozer]
log_level = 2
warn_on_root = 0
