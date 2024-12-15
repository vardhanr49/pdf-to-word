from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfReader
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

# Ensure upload and result folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    if 'pdf_file' not in request.files:
        return "No file part", 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return "No selected file", 400

    if pdf_file and pdf_file.filename.endswith('.pdf'):
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        word_path = os.path.join(app.config['RESULT_FOLDER'], pdf_file.filename.replace('.pdf', '.txt'))

        # Save the PDF file to the upload folder
        pdf_file.save(pdf_path)

        # Convert PDF to plain text
        try:
            reader = PdfReader(pdf_path)
            with open(word_path, 'w') as output_file:
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        output_file.write(text + "\n")
        except Exception as e:
            return f"Error during conversion: {str(e)}", 500

        return send_file(word_path, as_attachment=True)

    return "Invalid file type. Please upload a PDF.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
