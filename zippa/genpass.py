"""
Generates a (safeish) password.
"""
from secrets import token_bytes
from base64 import b64encode

PASSWORD_LENGTH=70

x = token_bytes(256)
print("{}".format(b64encode(x)[:PASSWORD_LENGTH]))