import hashlib
def hasher(item:tuple):
    plain_text = ",".join(item)
    return hashlib.sha256(plain_text)
