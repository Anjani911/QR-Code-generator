from flask import Flask, render_template, request, send_file
import qrcode
import os
from docx import Document

app = Flask(__name__, static_folder='static')

# Ensure the static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    # Get QR type from the form
    qr_type = request.form.get('qr_type')
    if not qr_type:
        return "No QR type selected", 400

    try:
        # Determine QR data based on the type
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
            if image.filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join('static', image.filename)
                image.save(image_path)
                qr_data = f"Image saved as {image.filename}"
            else:
                return "Invalid image format. Please upload JPG/JPEG/PNG.", 400

        elif qr_type == 'docx':
            doc_file = request.files['docfile']
            if doc_file.filename.endswith('.docx'):
                doc_path = os.path.join('static', doc_file.filename)
                doc_file.save(doc_path)
                doc = Document(doc_path)
                doc_text = "\n".join([para.text for para in doc.paragraphs])

                if not doc_text:
                    return "The document is empty.", 400

                qr_data = doc_text
            else:
                return "Invalid file format. Please upload a .docx file.", 400

        elif qr_type == 'pdf':
            pdf_file = request.files['pdffile']
            if pdf_file.filename.endswith('.pdf'):
                pdf_path = os.path.join('static', pdf_file.filename)
                pdf_file.save(pdf_path)

                # Generate a QR code linking to the PDF file
                qr_data = f"http://127.0.0.1:5000/static/{pdf_file.filename}"
            else:
                return "Invalid file format. Please upload a .pdf file.", 400

        else:
            return "Invalid QR type", 400

        # Generate and save the QR code
        img = qrcode.make(qr_data)
        qr_path = os.path.join(app.static_folder, 'qr.png')

        img.save(qr_path)
        print(f"QR code saved at: {qr_path}")

    except Exception as e:
        print(f"Error processing the request: {e}")
        return "Error generating QR code", 500

    return render_template('index.html', qr_path=f'/static/qr.png')

if __name__ == '__main__':
    app.run(debug=True)
