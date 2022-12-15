from leslie import f, verify
import sys

if len(sys.argv) != 4:
    print("Usage: python3 {} <public-key-file> <binary-to-verify> <signature-to-verify>".format(sys.argv[0]))
    exit(1)

keyfile = open(sys.argv[1], "rb")
tbsfile = open(sys.argv[2], "rb")
sigfile = open(sys.argv[3], "rb")
tbs = tbsfile.read()
key = keyfile.read()
sig = sigfile.read()
keyfile.close()
tbsfile.close()
sigfile.close()

h_tbs = f(tbs)
if verify(h_tbs, sig, key):
    print("Signature verified!")
else:
    print("Signature NOT verified!")