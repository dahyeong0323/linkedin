from __future__ import annotations

import base64
import hashlib


def _key_stream(secret: str, length: int) -> bytes:
    if not secret:
        secret = "change_me"
    seed = secret.encode("utf-8")
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(hashlib.sha256(seed + counter.to_bytes(4, "big")).digest())
        counter += 1
    return bytes(out[:length])


def encrypt_token(token: str, secret: str) -> str:
    raw = token.encode("utf-8")
    stream = _key_stream(secret, len(raw))
    encrypted = bytes(value ^ stream[index] for index, value in enumerate(raw))
    return base64.urlsafe_b64encode(encrypted).decode("ascii")


def decrypt_token(value: str, secret: str) -> str:
    encrypted = base64.urlsafe_b64decode(value.encode("ascii"))
    stream = _key_stream(secret, len(encrypted))
    raw = bytes(value ^ stream[index] for index, value in enumerate(encrypted))
    return raw.decode("utf-8")
