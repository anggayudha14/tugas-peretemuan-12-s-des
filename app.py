from flask import Flask, render_template, request
from sdes import encrypt, decrypt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    result = None
    steps = []
    mode = "encrypt"

    if request.method == "POST":

        text = request.form.get("text")
        key = request.form.get("key")
        mode = request.form.get("mode")

        if len(text) != 8:
            return render_template(
                "index.html",
                error="Input harus 8 bit"
            )

        if len(key) != 10:
            return render_template(
                "index.html",
                error="Key harus 10 bit"
            )

        if mode == "encrypt":
            result, steps = encrypt(text, key)
        else:
            result, steps = decrypt(text, key)

    return render_template(
        "index.html",
        result=result,
        steps=steps,
        mode=mode
    )

if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)