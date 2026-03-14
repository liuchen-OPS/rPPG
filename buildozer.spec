[buildozer]
# Buildozer configuration
warn_on_root = 0
log_level = 2

[app]

# (str) Title of your application
title = rPPG生理指标检测系统

# (str) Package name
package.name = heartrateapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,html,js,css

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 0.1

# (str) Application versioning (method 2)
# version.regex = __version__ = ['\"']([^'\"]+)['\"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.1.0,numpy,android,webview

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.1.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (string) Icon of the application
#android.icon = %(source.dir)s/data/icon.png

# (string) Round icon of the application
#android.round_icon = %(source.dir)s/data/icon.png

# (str) Target Android API, should be as high as possible.
#android.api = 31

# (str) Minimum API your APK will support.
#android.minapi = 21

# (str) Android SDK directory, if unset, it will be automatically located.
#android.sdk_path =

# (str) Android NDK directory, if unset, it will be automatically located.
#android.ndk_path =

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically located.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically located.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically located.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid an Internet connection or to use a local copy
# of the sdk.
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
#android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy based app.
#android.entrypoint = org.renpy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy based app.
#android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) List of Java libraries that will be added to the Android project.
# These libraries should be present in the libs/armeabi-v7a directory.
#android.add_libs_armeabi_v7a = libtensorflowlite_jni.so
#android.add_libs_armeabi = libtensorflowlite_jni.so
#android.add_libs_x86 = libtensorflowlite_jni.so
#android.add_libs_mips = libtensorflowlite_jni.so

# (list) List of Java libraries that will be added to the Android project.
# These libraries should be present in the libs/ directory.
#android.add_libs = libs/android/*.jar

# (list) JNI libraries to be added to the build
#android.add_jni = libs/android/*.so

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in the main activity
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a =

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi =

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 =

# (list) Android additional libraries to copy into libs/mips
#android.add_libs_mips =

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 =

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a =

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi =

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 =

# (list) Android additional libraries to copy into libs/mips
#android.add_libs_mips =

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 =

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android permissions
android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (int) Target Android API, should be as high as possible.
#android.api = 31

# (int) Minimum API your APK will support.
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically located.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically located.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically located.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid an Internet connection or to use a local copy
# of the sdk.
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
#android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy based app.
#android.entrypoint = org.renpy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy based app.
#android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) List of Java libraries that will be added to the Android project.
# These libraries should be present in the libs/armeabi-v7a directory.
#android.add_libs_armeabi_v7a = libtensorflowlite_jni.so
#android.add_libs_armeabi = libtensorflowlite_jni.so
#android.add_libs_x86 = libtensorflowlite_jni.so
#android.add_libs_mips = libtensorflowlite_jni.so

# (list) List of Java libraries that will be added to the Android project.
# These libraries should be present in the libs/ directory.
#android.add_libs = libs/android/*.jar

# (list) JNI libraries to be added to the build
#android.add_jni = libs/android/*.so

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in the main activity
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a =

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi =

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 =

# (list) Android additional libraries to copy into libs/mips
#android.add_libs_mips =

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 =

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a =

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi =

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 =

# (list) Android additional libraries to copy into libs/mips
#android.add_libs_mips =

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 =

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android permissions
#android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Android version to use
#android.minsdk = 21

# (int) Android version to use
#android.maxsdk = 0

# (int) Minimum API your APK will support.
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically located.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically located.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically located.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid an Internet connection or to use a local copy
# of the sdk.
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
#android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy based app.
#android.entrypoint = org.renpy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy based app.
#android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
#android.add_src =

# (list) List of Java libraries that will be added to the Android project.
# These libraries should be present in the libs/armeabi-v7a directory.
#android.add_libs_armeabi_v7a = libtensorflowlite_jni.so
#android.add_libs_armeabi = libtensorflowlite_jni.so
#android.add_libs_x86 = libtensorflowlite_jni.so
#android.add_libs_mips = libtensorflowlite_jni.so

# (list) List of Java libraries that will be added to the Android project.
# These libraries should be present in the libs/ directory.
#android.add_libs = libs/android/*.jar

# (list) JNI libraries to be added to the build
#android.add_jni = libs/android/*.so

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
#android.ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in the main activity
#android.manifest.intent_filters =

# (str) launchMode to set for the main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a =

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi =

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 =

# (list) Android additional libraries to copy into libs/mips
#android.add_libs_mips =

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 =

# (list) Android additional libraries to copy into libs/armeabi-v7a
#android.add_libs_armeabi_v7a =

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi =

# (list) Android additional libraries to copy into libs/x86
#android.add_libs_x86 =

# (list) Android additional libraries to copy into libs/mips
#android.add_libs_mips =

# (list) Android additional libraries to copy into libs/x86_64
#android.add_libs_x86_64 =

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
#android.wakelock = False

# (list) Android permissions
#android.permissions = CAMERA,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream (kivy)
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
#p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port =

#
# iOS specific
#

# (str) Path to a custom xcodebuild command to use
#ios.xcodebuild =

# (str) Xcode project configuration to use
#ios.configuration = Debug

# (str) Xcode project scheme to use
#ios.scheme =

# (bool) Whether to use the iOS simulator when building (requires Xcode 6.1+)
#ios.simulator = False

# (bool) Whether to use the iOS simulator when building (requires Xcode 6.1+)
#ios.simulator = False

# (bool) Whether to use the iOS simulator when building (requires Xcode 6.1+)
#ios.simulator = False

#
# Buildozer specific
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
#warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# buildozer build directory
#build_dir = .buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin directory
#bin_dir = bin

# -----------------------------------------------------------------------------
#
#  You can add or remove sections as you need
#
# -----------------------------------------------------------------------------