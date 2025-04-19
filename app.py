from flask import Flask, render_template, request
import os
from PIL import Image
import pytesseract
import PyPDF2
from PIL import Image

app = Flask(__name__)

# Config for file uploads
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to extract text from images (using pytesseract)
def extract_text_from_image(file_path):
    text = ''
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text

@app.route('/')
def index():
    return render_template('index.html')  # Homepage

@app.route('/about')
def about():
    return render_template('about.html')  # About Us Page

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Contact Us Page

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the file is in the request
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Process the file and generate a summary
        if file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(filename)
        elif file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            text = extract_text_from_image(filename)
        else:
            return 'Unsupported file type', 400
        
        # Create a summary of the extracted text (here we just limit the summary length)
        summary = text[:500] + "..."
        return render_template('index.html', summary=summary)  # Show the summary in the homepage

if __name__ == '__main__':
    app.run(debug=True)
