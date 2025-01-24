import hashlib
string = ("12","12","12")

digest = hashlib.sha512(",".join(string).encode('utf-8')).digest()
print(digest)

