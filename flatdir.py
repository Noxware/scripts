#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
from base64 import b32encode
from shutil import move


FLAT_DIR = Path('./Flattened')


def encode_int(i: int) -> str:
    """
    B32 based encoding for integers

    :param i: Int to encode
    :return: Encoded string
    """

    return b32encode(i.to_bytes(8, 'big').lstrip(b'\x00')).replace(b'=', b'').lower().decode()


def encoded_time() -> str:
    """Return a rounded timestamp encoded with encode_int() (len 7)"""

    return encode_int(int(datetime.now().timestamp()))


def safe_path(p: Path) -> Path:
    """
    If the target file already exists, a safe path with other name will be returned.
    Otherwise returns the Path passed as parameter.

    The safe path has a limit of 80 characters.

    :param p: Expected path
    :return: Unique path
    """

    if not p.exists():
        return p
    else:
        name = p.stem
        ext = p.suffix
        improbable = '_' + encoded_time()  # len 8

        # Total filename will have less than 80 chars.
        # 10 is 8 rounded
        max_name_len = 80 - len(ext) - 10
        new_p = p.parent / Path(name[0:max_name_len] + improbable + ext)

        if not new_p.exists():
            return new_p
        else:
            return safe_path(new_p)


def safe_move(source: Path, target: Path) -> None:
    """
    Moves a file using shutil.move(). If the target file already exists
    safe_path() will be used to get a new unique filename. The parent
    folder is created automatically if does not exist.
    """

    target.parent.mkdir(parents=True, exist_ok=True)
    move(source, safe_path(target))


def iter_subfiles(folder: Path):
    for p in folder.rglob('*'):
        if p.is_file():
            yield p


def main():
    for file in iter_subfiles(Path('.')):
        safe_move(file, FLAT_DIR / file.name)


if __name__ == '__main__':
    main()