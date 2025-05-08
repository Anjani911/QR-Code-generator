from flask import Flask, render_template, request, send_file
import qrcode
import os

app = Flask(__name__)

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    qr_type = request.form.get('qr_type')

 
    if qr_type == 'upi':
        payee = request.form['payee']
        name = request.form['name']
        amount = request.form.get('amount', '')
        upi_data = f"upi://pay?pa={payee}&pn={name}&am={amount}&cu=INR"
        qr_data = upi_data

    elif qr_type == 'wifi':
        ssid = request.form['ssid']
        password = request.form['password']
        encryption = request.form['encryption']
        wifi_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
        qr_data = wifi_data

    elif qr_type == 'link':
        qr_data = request.form['url']

    elif qr_type == 'image':
        image = request.files['image']
        image_path = os.path.join('static', image.filename)
        image.save(image_path)
        qr_data = f"Image saved as {image.filename}"  # Placeholder, as QR for images is not typical

    else:
        return "Invalid QR type", 400

    # Generate QR code
    img = qrcode.make(qr_data)
    qr_path = os.path.join('static', 'qr.png')
    img.save(qr_path)

    return render_template('index.html', qr_path=qr_path)

if __name__ == '__main__':
    app.run(debug=True)
