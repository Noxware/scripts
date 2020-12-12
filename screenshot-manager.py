#!/usr/bin/env python3


# Config (safe)
FORMAT = "JPG"
QUALITY = 80
DIR = "./Screenshots"


# Imports
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Slot
from win32gui import GetForegroundWindow
from win32process import GetWindowThreadProcessId
from pathlib import Path
import psutil


# Computed constants
DCAPTURES = Path(DIR)
FCOUNTER = DCAPTURES / ".idcount"


# Code
def increment_fid():
    current = None
    with open(FCOUNTER, 'r+') as f:
        current = f.readline()
        next = int(current) + 1
        f.seek(0)
        f.write(str(next))
        f.flush()
    return current


def init_files():
    DCAPTURES.mkdir(parents=True, exist_ok=True)

    if not FCOUNTER.is_file():
        with open(FCOUNTER, 'w') as f:
            f.write("0")
            f.flush()


def top_window_process():
    window = GetForegroundWindow()
    tid, pid = GetWindowThreadProcessId(window)
    pname = psutil.Process(pid).name()
    return str(Path(pname).with_suffix(""))


@Slot()
def clipboard_data_changed():
    clipboard = QApplication.clipboard()
    image = clipboard.image()
    if not image.isNull():
        init_files()
        pfolder = DCAPTURES / top_window_process()
        pfolder.mkdir(parents=True, exist_ok=True)
        filename = f"{increment_fid()}.{FORMAT.lower()}"
        image.save(str(pfolder / filename), FORMAT, QUALITY)


def main():
    init_files()
    app = QApplication()
    clipboard = QApplication.clipboard()
    clipboard.changed.connect(clipboard_data_changed)
    app.exec_()


if __name__ == "__main__":
    print('Running...')
    main()
    print('Stopped...')
