from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Set the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    filename = ""
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        file = request.files.get('file')

        # Validation: Check if name and file are provided
        if not name or not file or not file.filename:
            return render_template('index.html', message="Please enter your name and select a file!")
        
        # File handling
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            message = 'File selected successfully!'
        else:
            message = 'Invalid file format. Please upload a valid image.'

    return render_template('index.html', message=message, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
