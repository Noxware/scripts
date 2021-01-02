# Scripts

This repo contains very very small utility scripts that sometimes I use.

## adb-wifi.py

Guided configuration of adb over wifi. Useful for debugging mobile apps
in a real device without an usb cable. A cable is still necessary for
the initial setup.

## ext-fix.py

Check the mime type of all files in the current directory. If those files have a wrong (or missing) file extension, this script can add the correct extension to the file name. (The original extension is preserved as part of the filename).

> Depends on 'filetype'.

## screenshot-manager.py

Every time a screenshot is placed in the clipboard, this script saves it
in a small JPG file (customizable) inside a folder with the name of the 
process of the active window.

> Only working on Windows. Depends on 'pyside6', 'pywin32' and 'psutil'.

## urlopen.py

Having a list of urls (separated by spaces or new line characters) copied
in your clipboard, run this script to open all those urls.

> Depends on 'pyperclip'.

## flatdir.py

Generates a folder called 'Flattened' containing every file in the current
folder and its sub folders.