from flask import Flask, request, render_template, send_file, url_for
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
	qr_url = None
	if request.method == 'POST':
		link = request.form['link']
		logo = request.files.get('logo')
		output_filename = 'generated_qr_code.png'
		output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

		logo_path = None
		if logo:
			logo_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(logo.filename))
			logo.save(logo_path)

		try:
			generate_custom_qr_code(link, logo_path, output_path)
			qr_url = url_for('static', filename=f'uploads/{output_filename}')
		finally:
			if logo_path and os.path.exists(logo_path):
				os.remove(logo_path)

	return render_template('index.html', qr_url=qr_url)

@app.route('/download', methods=['GET'])
def download():
	output_filename = 'generated_qr_code.png'
	output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

	if os.path.exists(output_path):
		try:
			return send_file(output_path, as_attachment=True)
		finally:
			# Ensure the QR code is deleted after being served
			if os.path.exists(output_path):
				os.remove(output_path)
	else:
		return "File not found", 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 10000))
	app.run(host='0.0.0.0', port=port, debug=True)
