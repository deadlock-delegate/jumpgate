import os


def generate_rand() -> bytes:
    return os.urandom(32)
