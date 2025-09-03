from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import send_from_directory
import os
import shutil


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    arquivos = os.listdir(UPLOAD_FOLDER)
    return render_template('ideia.html', arquivos=arquivos)

@app.route('/download/<filename>')
def download(filename):
    caminho_upload = os.path.join(UPLOAD_FOLDER, filename)
    caminho_download = os.path.join(DOWNLOAD_FOLDER, filename)

    # Só copia se ainda não existir na pasta downloads
    if not os.path.exists(caminho_download):
        shutil.copy(caminho_upload, caminho_download)

    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'arquivo' not in request.files:
        return "no file sent", 400

    arquivo = request.files['arquivo']

    if arquivo.filename == '':
        return "Invalid file syntax", 400
    
    caminho_upload = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho_upload)
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5501)
