import hashlib

def genMD5(input):
    return hashlib.md5(input.encode()).hexdigest()