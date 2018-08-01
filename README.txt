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
    https://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files (follow the instructions of the top-voted answer)
    https://legacy.imagemagick.org/script/binary-releases.php#windows
    http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html
    https://cmake.org/download/
    https://github.com/smeucci/LineSegm/blob/master/create_groundtruth.py

This code converts scanned PDFs, JPGs and PNGs into text.
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
Email: rafaelichow@gmail.com / faelchow@hotmail.com
Phone: +55 11 99210-4192
