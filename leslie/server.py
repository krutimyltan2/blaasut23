from flask import Flask, request, jsonify
from leslie import verify, f, F_LEN_BYTES, k
app = Flask(__name__)

f = open("public_key.bin", "rb")
public_key = f.read()
f.close()

public_files={"server.py", "public_key.bin", "leslie.py", "signer.py", "verifier.py"}
private_files={"flagga.txt"}

@app.route("/", methods=["GET"])
def get_public_files():
    rsp = {"public_files": public_files, "msg": "Use GET /file/<filename> to get a file."}
    return jsonify(rsp)

@app.route("/file/<str:filename>", methods=["GET"])
def get_public_file(filename):
    if filename in public_files:
        return jsonify(f.open(filename, "rb").read())
    return jsonify("No such public file.")

@app.route("/upload", methods=["POST"])
def upload_trusted_list():
    js = request.json
    if not "msg" in js:
        return jsonify("No file list found.")
    if not isinstance(js["msg"], bytes):
        return jsonify("Wrong file list type (should be bytes).")
    if not len(js["msg"]) <= 512:
        return jsonify("File list too big.")
    if not "sgn" in js:
        return jsonify("No signature found in request.")
    if not isinstance(js["sgn"], bytes):
        return jsonify("Bad signature type.")
    if not len(js["sgn"]) == F_LEN_BYTES * k:
        return jsonify("Wrong signature length.")
    h_f = f(js["msg"])
    if verify(h_f, js["sig"], public_key):
        split_msg = js["msg"].split(b",")
        for filename in split_msg:
            s_filename = filename.decode()
            if (not s_filename in public_files) and (s_filename in private_files):
                public_files.add(s_filename)
                private_files.remove(s_filename)

if __name__ == '__main__':
    app.run()