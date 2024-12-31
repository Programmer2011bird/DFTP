import hashlib


def calculate_sha256(content:str) -> str:
    hash = hashlib.sha256()
    hash.update(content.encode())

    return hash.hexdigest()
