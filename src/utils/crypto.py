import bcrypt


def hash_password(password: str, rounds=12):
    salt = bcrypt.gensalt(rounds=rounds)
    bytes_pwd = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(bytes_pwd, salt)
    if hashed_password:
        return hashed_password.decode('utf-8')
    raise Exception("Hash password: unexpected behavior")


def validate_password(password: str, password_hash):
    bytes_pwd = password.encode('utf-8')
    hash_pwd = password_hash.encode('utf-8')
    result = bcrypt.checkpw(bytes_pwd, hashed_password=hash_pwd)
    return result
