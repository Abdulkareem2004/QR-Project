from flask import Flask, render_template, request, redirect, flash
import pandas as pd
import os
import qrcode

# Replace this with your actual URL when hosted
url = 'http://127.0.0.1:5000'

# Create QR Code
qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)
qr.add_data(url)
qr.make(fit=True)

# Generate image
img = qr.make_image(fill_color='black', back_color='white')

# Save image
img.save('form_qr.png')

print("✅ QR Code generated and saved as form_qr.png")


app = Flask(__name__)
app.secret_key = 'secret'

EXCEL_FILE = 'data.xlsx'

# Create Excel if not exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Month", "Name", "Amount"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    month = request.form['month']
    name = request.form['name']
    amount = request.form['amount']

    if not (month and name and amount):
        flash("⚠️ All fields are required!")
        return redirect('/')

    try:
        new_data = pd.DataFrame([[month, name, amount]], columns=["Month", "Name", "Amount"])
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        flash("✅ Data saved successfully!")
    except Exception as e:
        flash(f"❌ Error: {e}")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
