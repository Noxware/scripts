from os import system

# (Windows) Bluestacks
# https://stackoverflow.com/questions/54317727/how-do-you-adb-to-bluestacks-4
system('adb connect localhost:5555')

# (Windows) Netease Mumu
# https://airtest.doc.io.netease.com/en/IDEdocs/device_connection/3_emulator_connection/
system('adb connect localhost:7555')

system('adb devices')