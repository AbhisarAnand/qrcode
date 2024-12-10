from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
from utils import generate_custom_qr_code

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB limit for uploads

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		link = request.form['link']
		logo = request.files.get('logo')
		output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_qr_code.png')

		if logo:
			logo_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(logo.filename))
			logo.save(logo_path)
			generate_custom_qr_code(link, logo_path, output_path)
			os.remove(logo_path)  # Clean up the uploaded logo
		else:
			generate_custom_qr_code(link, None, output_path)

		return send_file(output_path, as_attachment=True)

	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)