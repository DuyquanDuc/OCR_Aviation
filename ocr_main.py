import pytesseract
from PIL import Image
import os

# Set the directory 
data_directory = './Data'
output_directory = './ocr_main_output'

# Set the path 
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\DuyQD\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' 
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract' # for MacOS or Linux

def ocr_on_image(image_path):
    '''image_to_string on specified image file and return the text extracted from the image.'''
    try:
        # Open the image file
        img = Image.open(image_path)
        # Use tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return ""


# Loop over all the images in the directory
for image_filename in os.listdir(data_directory):
    if image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(data_directory, image_filename)
        print(f"Processing {image_filename}...")
        try:
            text = ocr_on_image(image_path)
            # Define the path for the output text file
            text_file_path = os.path.join(output_directory, image_filename + '.txt')
            # Write the extracted text into a .txt file
            with open(text_file_path, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Text written to {text_file_path}")
        except Exception as e:
            print(f"Failed to process {image_filename} due to {e}")
        print("-" * 50)
