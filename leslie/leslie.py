"""
Implementation av Leslie-signaturer.
Se https://en.wikipedia.org/wiki/Lamport_signature för mer information.
"""
import secrets
import hashlib

SHA3_512_DIGEST_LEN_BITS = 512
SHA3_512_DIGEST_LEN_BYTES = (SHA3_512_DIGEST_LEN_BITS//8)
F_LEN_BITS = SHA3_512_DIGEST_LEN_BITS
F_LEN_BYTES = (SHA3_512_DIGEST_LEN_BITS//8)
k = SHA3_512_DIGEST_LEN_BITS

def f(y_ij):
    """SHA3-512 är en förmodad envägsfunktion"""
    return hashlib.sha3_512(y_ij).digest()

def generate_private_key():
    by = secrets.token_bytes(2*k)
    return by

def generate_public_key(private_key):
    by = b""
    for i in range(k):
        for j in [0,1]:
            by += f(private_key[2*i + j:2*i + j + 1])
    return by

def get_js(msg):
    return [(mb >> s) & 0b1 for s in range(7,-1,-1) for mb in msg]

def sign(msg, private_key):
    assert(len(msg) == k//8)
    js = get_js(msg)
    assert(len(js) == k)
    sign = b""
    for i in range(k):
        j = js[i]
        y_ij = private_key[2*i + j : 2*i + j + 1]
        sign += f(y_ij)
    return sign

def verify(msg, signature, public_key):
    js = get_js(msg)
    if(len(js) != k):
        return False
    for i in range(k):
        j = js[i]
        f_y_ij = signature[i*F_LEN_BYTES : (i+1)*F_LEN_BYTES]
        if f_y_ij != public_key[(2*i + j)*F_LEN_BYTES : (2*i + j + 1)*F_LEN_BYTES]:
            return False
    return True

if __name__ == "__main__":
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    msg = f(b"hello_world")
    s = sign(msg, private_key)
    print(verify(msg, s, public_key))