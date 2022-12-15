from leslie import generate_private_key, generate_public_key

private_key = generate_private_key()
public_key = generate_public_key(private_key)

f = open("private_key.bin", "wb")
f.write(private_key)
f.close()
f = open("public_key.bin", "wb")
f.write(public_key)
f.close()