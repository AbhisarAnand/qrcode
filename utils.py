import qrcode
from PIL import Image

def generate_custom_qr_code(link, logo_path, output_path):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=10,
		border=4,
	)
	qr.add_data(link)
	qr.make(fit=True)

	qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

	if logo_path:
		logo = Image.open(logo_path)
		logo_size = int(qr_img.size[0] * 0.25)
		logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
		pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
		qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

	qr_img.save(output_path)