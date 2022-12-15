import pyzipper

kakburk = "exposed/kakburk.zip"
admin_username = "admin"
usersfile = "users.txt"
flagfile = "flagga.txt"

def get_flagga():
    f = open(flagfile, "r")
    for l in f.readlines():
        if l[-1] == "\n":
            l = l[:-1]
        f.close()
        return l

def get_admin_password():
    f = open(usersfile, "r")
    for l in f.readlines():
        if l[-1] == "\n":
            l = l[:-1]
        ls = l.split(",")
        if ls[0] == admin_username:
            f.close()
            return ls[1].encode()

with pyzipper.AESZipFile(kakburk, "w", compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
    zf.setpassword(get_admin_password())
    zf.writestr("flagga.txt", get_flagga())