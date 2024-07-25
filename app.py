from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
#pip install Flask
app = Flask(__name__)
app.secret_key = 'key'

UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

REGISTO_FILE = 'registo.txt'

def save_registo(data_hora, nome_real):
    with open(REGISTO_FILE, 'a') as file:
        file.write(f"{data_hora},{nome_real}\n")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file:
            data_hora = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{data_hora}_{file.filename}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            save_registo(data_hora, file.filename)
            flash('File successfully uploaded', 'success')
            return redirect(url_for('upload_file'))
    
    return render_template('upload.html')
print("\x1bc\x1b[47;34m")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

