import os
import glob
import imghdr
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from colorthief import ColorThief

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', ".jpeg"]
app.config['UPLOAD_PATH'] = 'static/uploads'

color_platte = []
uploadfile = ""

def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    # files = os.listdir(app.config['UPLOAD_PATH'])
    files = uploadfile
    colors = color_platte
    print(files)
    return render_template('index.html', files=files, colors=colors)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    
    color_platte.clear()
    upf = "static/uploads/" + filename
    global uploadfile
    uploadfile = filename
    color_thief = ColorThief(upf)
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=5)
    for color in palette:
        color_platte.append(color)
    print(color_platte)

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

if __name__ == "__main__":
    app.run(debug=True)