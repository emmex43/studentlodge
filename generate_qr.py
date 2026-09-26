import qrcode

# 1. Set the destination URL (this is permanent once generated!)
data = "https://studentlodge.com.ng"

# 2. Configure the QR code's look and error correction
qr = qrcode.QRCode(
    version=1, # Size of the QR code (1 is smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_H, # High error correction so it scans easily even if slightly damaged
    box_size=10, # Pixel size of each box
    border=4, # Thickness of the white border
)

# 3. Add the data and compile
qr.add_data(data)
qr.make(fit=True)

# 4. Create and save the image file
img = qr.make_image(fill_color="black", back_color="white")
img.save("website_qr_code.png")

print("Success! Your permanent QR code is saved as website_qr_code.png.")