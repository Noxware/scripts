from pyperclip import paste
from webbrowser import open
import sys
import re


def main():
    text: str = paste()

    if text == "":
        sys.exit("No text in clipboard.")

    urls = re.split(r"[ \n]", text)
    for u in urls:
        open(u, new=2, autoraise=True)


if __name__ == '__main__':
    main()