from flask import Flask, render_template, request, send_file
from io import BytesIO
from Generate_Qr import QrCode   # importa tu clase QrCode

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    url = None
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not url:
            error = "Por favor ingresa una URL válida."
            url = None
    return render_template("index.html", url=url, error=error)

@app.route("/qr_image")
def qr_image():
    url = request.args.get("url", "").strip()
    if not url:
        return "Falta parámetro URL", 400
    # Genera el QR usando tu propio módulo
    qr = QrCode.encode_text(url, QrCode.Ecc.MEDIUM)
    img = QrCode.render_qr_to_image(qr, scale=10, border=4)
    # Envía la imagen en memoria
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
