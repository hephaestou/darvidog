[app]

# App information
title = Darvidog Soil Analyser
package.name = darvidog
package.domain = com.gaiandynamics

# Source code
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Version
version = 1.0

# Requirements
requirements = python3,kivy,kivymd,plyer



# Permissions
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FLASHLIGHT

# Features
android.features = android.hardware.camera

# Orientation
orientation = portrait

# App icon - black labrador logo
icon.filename = %(source.dir)s/icon.png

# Splash screen
#presplash.filename = %(source.dir)s/splash.png

[buildozer]

# Log level
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1
