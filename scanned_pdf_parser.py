"""
Prior to running this code, please install:

pip install pillow
pip install pytesseract
pip install wand

https://sourceforge.net/projects/opencvlibrary/files/

Also intall:
Linux:
    sudo apt-get install tesseract-ocr
    sudo apt-get install libmagickwand-dev

Windows:
    https://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files
    https://legacy.imagemagick.org/script/binary-releases.php#windows
    http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
    https://cmake.org/download/
    https://github.com/smeucci/LineSegm/blob/master/create_groundtruth.py

This code converts scanned PDFs, JPGs and PNGs into text.
Parameter must be manually adapted to fit the sample of the pdf that is going to be parsed.
The optimal procedure is to slice the original pdf into smaller parts:
    - i.e if a document follows a pattern of having the information of interest in the second part of the
    first page, the best practice should be to slice that part and then apply the methods of this class.
    The reason for this is that it's not guaranteed that this code will work on PDFs that contain images.

### NOTES:
1 - pytesseract for Windows isn't working very well. I had to call tesseract directly from the terminal.
2 - This code is not optimal for any kind of PDFs. Some more image thresholds adjustments might be necessary to tune the
quality of images at the "remove_noise" method. Further exaplanation of what's happening in this method can
be found at https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#adaptive-thresholding
Note that since tesseract doesn't accept binary tresholds, the best method is probably "adaptive Gaussian", though more tests
are needed.

Author: Rafael Inaimo Chow
Email: rafaelichow@gmail.com
Phone: +55 11 99210-4192
"""
from matplotlib import pyplot as plt
from wand.image import Image as Img
from PyPDF2 import PdfFileReader
from PIL import Image
import numpy as np
import pytesseract
import subprocess
import platform
import time
import sys
import cv2
import os


if platform.system() == 'Windows':
    ### Sets pytesseract's path on Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'
    tessdata_dir_config = r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'

class ParseScannedPdf(object):
    ### Ideally, it would be optimal to have an Enviroment Variable to avoid the line below.
    if platform.system() == 'Windows':
        ### Class variable with the temp folder.
        pdf_folder = os.path.join(os.getcwd(), 'pdf_and_images')
        temp_folder = os.path.join(os.getcwd(), 'temp')
        output_folder = os.path.join(os.getcwd(), 'output')

    def __init__(self, file=None, lang='eng'):
        self.file = file
        self.lang = lang
        ### Self.img_file is set equal to self_file at the beginning of the script.
        ### In case self.file is a pdf, self.img_file will be set to the png version
        self.img_file = self.file
        self.type_pdf = False

        @property
        def file(self):
            return self.file

        @file.setter
        def file(self, value):
            self.file = value

        @property
        def lang(self):
            return self.lang

        @lang.setter
        def lang(self, value):
            self.lang = value

    def pdf_resolution(self):
        """
        Getting the PDF's resolution can be useful in the future when setting the resolution parameter
        in the "convert_scanned_pdf_to_png" method.
        :return: resolution of pdf file, as a tuple.
        """
        resolution = PdfFileReader(open(self.file, 'rb'))  ### Gets pdf's resolution
        x_res = resolution.getPage(0).mediaBox[-2]
        y_res = resolution.getPage(0).mediaBox[-1]
        resolution = (x_res, y_res)
        return resolution

    def convert_scanned_pdf_to_png(self):
        """
        Resolution = 300 and compression_quality = 99 are optimal to assure the image's quality.
        :return: file converted to JPG
        """

        img = Img(filename=self.file, resolution=300) ### Opens scanned pdf file
        img.compression_quality = 99 ### Sets compression quality to 72

        ### Reassign self.img_file according to self.file
        try:
            self.img_file = self.file.split('/')[-1]
            self.img_file = self.img_file.replace('.pdf', '.png')
            self.img_file = os.path.join(ParseScannedPdf.temp_folder, self.img_file)
        except Exception as e:
            print 'Be sure to use forward slash when assigning the path of the pdf or img file.'
            print e.args
            sys.exit()

        self.type_pdf = True
        img.save(filename=self.img_file)  ### Converts the file to png
        time.sleep(2)

    def remove_noise(self):
        """
        :return: png file with removed noise
        """
        ### Read image with opencv
        if self.type_pdf: ### Case original file was a PDF
            img = cv2.imread(os.path.join(ParseScannedPdf.temp_folder, self.img_file))
        else: ### Case original file was a PNG or JPG
            img = cv2.imread(os.path.join(ParseScannedPdf.pdf_folder, self.img_file.split('/')[-1]))

        ### Convert to gray scale
        ### Essentially, the line below converts colored images to black and white.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ### Apply dilation and erosion to remove some noise
        ### An explanation of what the lines below are doing can be found here:
        ### https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=2)
        img = cv2.erode(img, kernel, iterations=1)

        ### Write image after removed noise
        cv2.imwrite(os.path.join(ParseScannedPdf.temp_folder, "removed_noise.png"), img)
        time.sleep(2)
        #self.img = img

    def convert_png_to_text(self):
        """
        :return: the conversion of the png to text
        """
        ### Runs tesseract
        if platform.system() == 'Windows':
            subprocess.call('C:\Program Files (x86)\Tesseract-OCR/tesseract.exe -l '
                      + self.lang + ' ' + self.img_file + ' ' +
                      os.path.join(ParseScannedPdf.output_folder, 'text'))

        else: ### For *nix (Must be tested furrther):
            os.system('tesseract -l ' + self.lang + ' ' + self.img_file + ' '
                      + os.path.join(ParseScannedPdf.output_folder, 'text'))

    def clean_temp_folder(self):
        """
        :return: cleans temp folder
        """
        for file in os.listdir(ParseScannedPdf.temp_folder):
            file_path = os.path.join(ParseScannedPdf.temp_folder, file)
            os.unlink(file_path)

    def convert_pdf_to_text(self):
        """
        :return: main function.
        """
        if self.file.endswith(('pdf', 'PDF')):
            ParseScannedPdf.convert_scanned_pdf_to_png(self)
        ParseScannedPdf.remove_noise(self)
        ParseScannedPdf.convert_png_to_text(self)
        ParseScannedPdf.clean_temp_folder(self)

if __name__=='__main__':
    ### Even on Windows, the sep must be '/'
    pdf = 'pdf_and_images/stoicism.png'
    converter = ParseScannedPdf(file=pdf)
    converter.convert_pdf_to_text()
