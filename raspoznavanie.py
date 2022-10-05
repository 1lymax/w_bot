from PIL import Image
from pytesseract import image_to_string
import pytesseract

tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'
pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 

#print image_to_string(Image.open('test.png'))
print (image_to_string(Image.open('var/2/coordinates.png'), lang='eng', config=tessdata_dir_config))