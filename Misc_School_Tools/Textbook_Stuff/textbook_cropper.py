import fitz  # PyMuPDF
import os
import pytesseract
from PIL import Image

# COMMAND TO RUN:
# /c/Users/zenit/AppData/Local/Programs/Python/Python310/python.exe textbook_cropper.py

# Load the PDF
pdf_path = "Chegg_ The Regional Toolkit(197-201).pdf"
doc = fitz.open(pdf_path)

# Define the crop margins (adjust as necessary)
bottom_crop_margin = 105  # Adjust this to the margin you want to remove from the bottom
top_crop_margin_first_page = 100  # Adjust this for the top margin on the first page

# Step 1: Crop the PDF
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)

    # Get the current page rectangle dimensions
    rect = page.rect

    # For the first page: remove both top and bottom parts
    if page_num == 0:
        new_rect = fitz.Rect(rect.x0, rect.y0 + top_crop_margin_first_page, rect.x1, rect.y1 - bottom_crop_margin)
    # For other pages: remove only the bottom part
    else:
        new_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1 - bottom_crop_margin)

    # Apply the crop to the page
    page.set_cropbox(new_rect)

# Step 2: Save each cropped page as a screenshot (image)

# Set the zoom level for higher resolution (1.5 means 150% zoom, adjust as needed)
zoom = 1.5  # 1.5x zoom gives higher resolution images
matrix = fitz.Matrix(zoom, zoom)

# Define the output directory path
output_dir = r"C:\Users\zenit\BYUSchoolCoding\Textbook_Stuff"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Create a file to store the extracted text
output_text_file = os.path.join(output_dir, "extracted_text197-201.txt")

# Step 3: Extract text from each image after saving

with open(output_text_file, "w", encoding="utf-8") as text_file:
    # Iterate over all pages again to save them as images and extract text
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Load each cropped page

        # Render the page to an image with the specified zoom
        pix = page.get_pixmap(matrix=matrix)

        # Construct the output file path for each page image
        output_image_path = os.path.join(output_dir, f"cropped_page_{page_num + 1}.png")

        # Save each page as a PNG file
        pix.save(output_image_path)

        # Step 4: Extract text from the saved image using pytesseract
        extracted_text = pytesseract.image_to_string(Image.open(output_image_path))

        # Write the extracted text to the file (preserving formatting)
        text_file.write(f"\n--- Page {page_num + 1} ---\n")
        text_file.write(extracted_text)

# Close the document
doc.close()
