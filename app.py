import csv
import qrcode
from itertools import islice
from PIL import Image, ImageOps, ImageDraw, ImageFont

# Open the CSV file and read its contents
with open('EAST_Building_Assets_FY66.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    
    # Skip the first line of the CSV file (assumes it contains headers)
    next(reader)

    # Slice the iterable to limit to 5 rows
    # limited_reader = islice(reader, 1)
  
    # for row in limited_reader:
    for row in reader:

        # Get the data from the CSV row
        data = '\n'.join(row)


        # Generate a QR code for the data
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        # Save the QR code as a PNG image
        img = qr.make_image(fill_color="black", back_color="white")
        # img.save(f"QR/{row[0]}.png")


        # Add a 10-pixel-wide black frame on top
        img_with_frame = ImageOps.expand(img, border=(0, 10), fill="black")

        # Get the font for the text
        font = ImageFont.truetype("arial.ttf", size=20) 

        # Create a new image with a white background to hold the text
        text_img = Image.new("RGB", (img_with_frame.width, 50), color="white")

        # Draw the text onto the new image
        draw = ImageDraw.Draw(text_img)
        text = row[1]  # Assumes that the data to overlay is in the second column
        text_width, text_height = draw.textsize(text, font=font)
        x = (text_img.width - text_width) / 2
        y = (text_img.height - text_height) / 2
        draw.text((x, y), text, font=font, fill="black")

        # Combine the QR code image and the text image
        result_img = Image.new("RGB", (img_with_frame.width, img_with_frame.height + text_img.height), color="white")
        result_img.paste(img_with_frame, (0, 0))
        result_img.paste(text_img, (0, img_with_frame.height))

        # Save the resulting image
        result_img.save(f"QR/{row[0]}.png")