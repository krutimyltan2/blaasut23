from flask import Flask, request, jsonify
from leslie import verify, f, F_LEN_BYTES, k
app = Flask(__name__)

f = open("public_key.bin", "rb")
public_key = f.read()
f.close()

@app.route('/upload', methods=['POST'])
def upload_trusted_software():
    js = request.json
    if not "msg" in js:
        return jsonify("No software found.")
    if not type(js["msg"]) == bytes:
        return jsonify("Wrong software type")
    if not len(js["msg"] <= 512):
        return jsonify("Software too big.")
    if not "sgn" in js:
        return jsonify("No signature found in request.")
    if not type(js["sgn"]) == bytes:
        return jsonify("Bad signature type.")
    if not len(js["sgn"]) == F_LEN_BYTES * k:
        return jsonify("Wrong signature length.")
    h_f = f(js["msg"])
    if verify(h_f, js["sig"], public_key):
        result = None
        exec("result = {}".format(js["msg"].decode()))
        return jsonify(result)

if __name__ == '__main__':
    app.run()