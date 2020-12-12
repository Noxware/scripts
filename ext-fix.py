#!/usr/bin/env python3

# Imports
import sys
from pathlib import Path

try:
    import filetype
except ModuleNotFoundError:
    sys.exit("'filetype' module not found. Please install it with 'pip install filetype'")
except Exception as ex:
    sys.exit(str(ex))


# Code
def ask_confirmation():
    yes = {"yes", "y"}

    ans = input("Write 'yes' or 'y' to confirm. Otherwise the operation will be aborted. ")

    if ans in yes:
        return True
    else:
        print("Operation aborted.")
        return False


def main():
    file_real_ext_map = {}

    for p in Path('.').iterdir():
        if p.is_file():
            cur_ext = p.suffix
            file_kind = filetype.guess(str(p))

            if file_kind is None:
                continue

            real_ext = "." + file_kind.extension

            if cur_ext != real_ext:
                print(f"'{p}' should have a '{real_ext}' extension.")
                file_real_ext_map[p] = real_ext

    print("\nThis script will add the correct file extension to each file. The older extension will be preserved as "
          "part of the filename. Are you ok with this?")

    if ask_confirmation():
        for p, ext in file_real_ext_map.items():
            p.rename(p.with_suffix(p.suffix + ext))
        print("Done.")


if __name__ == "__main__":
    main()
