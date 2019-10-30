import hashlib


class Hashing:

    @staticmethod
    def md5Hashing(value: str):
        messageDigest = hashlib.md5()
        messageDigest.update(value.encode('utf-8'))
        return str(messageDigest.hexdigest())
