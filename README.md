# TextReconition
A simple text reconizer that translates images to text (OCR).

It uses OpenCV2 to conver image pixels into np.arrays and tesseract to interpret those arrays.

This code converts scanned PDFs, JPGs and PNGs into text.

Parameter must be manually adapted to fit the sample of the pdf that is going to be parsed.
The optimal procedure is to slice the original pdf into smaller parts:
    - i.e if a document follows a pattern of having the information of interest in the second part of the
    first page, the best practice should be to slice that part and then apply the methods of this class.
    The reason for this is that it's not guaranteed that this code will work on PDFs that contain images.

# Installation
Prior to running this code, please install:
pip install pillow
pip install pytesseract
pip install wand
https://sourceforge.net/projects/opencvlibrary/files/

Also intall:
<p>Linux:</p>
    - sudo apt-get install tesseract-ocr
    && sudo apt-get install libmagickwand-dev

<p></p>
<p>Windows:</p>
    <p>- https://stackoverflow.com/questions/13984357/pythonmagick-cant-find-my-pdf-files</p>
    <p>- https://legacy.imagemagick.org/script/binary-releases.php#windows</p>
    <p>- http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html</p>
    <p>- https://cmake.org/download/</p>
    <p>- https://github.com/smeucci/LineSegm/blob/master/create_groundtruth.py</p>

# NOTES:
1 - pytesseract for Windows isn't working very well. I had to call tesseract directly from the terminal.
<p>2 - This code is not optimal for any kind of PDFs. Some more image thresholds adjustments might be necessary to tune the
quality of images at the "remove_noise" method. Further exaplanation of what's happening in this method can
be found at https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#adaptive-thresholding</p>

Note that since tesseract doesn't accept binary tresholds, the best method is probably "adaptive Gaussian", though more tests
are needed.
