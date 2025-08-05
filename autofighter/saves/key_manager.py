import base64
import hashlib
import os
import shutil
from pathlib import Path

_ITERATIONS = 100_000
_KEY_LEN = 32


def derive_key(password: str, salt: bytes | None = None) -> tuple[str, bytes]:
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _ITERATIONS, _KEY_LEN)
    return key.hex(), salt


def save_salt(path: Path, salt: bytes) -> None:
    path.write_text(base64.b64encode(salt).decode())


def load_salt(path: Path) -> bytes:
    data = path.read_text()
    return base64.b64decode(data.encode())


def backup_key_file(src: Path, dest: Path) -> None:
    shutil.copy2(src, dest)


def restore_key_file(src: Path, dest: Path) -> None:
    shutil.copy2(src, dest)
