import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import datetime

from core.file_parser import parse_pdf, parse_txt
from core.content_processor import process_content
from core.podcast_generator import generate_podcast_script
from core.tts_handler import generate_podcast_audio

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'input_materials'
OUTPUT_FOLDER = 'output_podcasts'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            input_filename = f"{timestamp}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
            file.save(file_path)

            # Process the file
            text_content = ""
            if filename.lower().endswith('.pdf'):
                text_content = parse_pdf(file_path)
            elif filename.lower().endswith('.txt'):
                text_content = parse_txt(file_path)

            processed_material = process_content(text_content)
            podcast_script_text = generate_podcast_script(processed_material)
            
            # For the script display, we can just pass the text
            # For audio generation, we pass the script lines (which generate_podcast_script returns as a single string for now)
            script_lines = podcast_script_text.split('\n')


            output_basename = f"{timestamp}_{os.path.splitext(filename)[0]}"
            audio_file_path = generate_podcast_audio(script_lines, output_basename, app.config['OUTPUT_FOLDER'])

            if audio_file_path:
                # relative path for URL
                audio_file_url = os.path.join(app.config['OUTPUT_FOLDER'], os.path.basename(audio_file_path))
                # remove the initial 'output_podcasts/' for the url_for
                # audio_file_url_for_template = audio_file_path.replace(app.config['OUTPUT_FOLDER'] + os.sep, "")
                return render_template('result.html', 
                                       script=podcast_script_text, 
                                       audio_url=audio_file_url, 
                                       filename=filename)
            else:
                return "Error generating audio.", 500

    return render_template('upload.html')

@app.route('/output_podcasts/<filename>')
def serve_podcast(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True) 