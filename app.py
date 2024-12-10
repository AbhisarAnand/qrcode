from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
from utils import generate_custom_qr_code

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB limit for uploads

if not os.path.exists(app.config['UPLOAD_FOLDER']):
	os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		link = request.form['link']
		logo = request.files.get('logo')
		output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_qr_code.png')

		logo_path = None
		if logo:
			logo_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(logo.filename))
			logo.save(logo_path)

		try:
			generate_custom_qr_code(link, logo_path, output_path)
			return send_file(output_path, as_attachment=True)
		finally:
			if logo_path and os.path.exists(logo_path):
				os.remove(logo_path)
			if os.path.exists(output_path):
				os.remove(output_path)

	return render_template('index.html')

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 10000))
	app.run(host='0.0.0.0', port=port, debug=True)
