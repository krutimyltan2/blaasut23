from leslie import f, sign
import sys

if len(sys.argv) != 3:
    print("Usage: python3 {} <private-key-file> <binary-to-sign>".format(sys.argv[0]))
    exit(1)

keyfile = open(sys.argv[1], "rb")
tbsfile = open(sys.argv[2], "rb")
tbs = tbsfile.read()
key = keyfile.read()
keyfile.close()
tbsfile.close()

h_tbs = f(tbs)
s = sign(h_tbs, key)
sys.stdout.buffer.write(s)