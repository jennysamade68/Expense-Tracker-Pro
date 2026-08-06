import pytesseract
from PIL import Image
import cv2
import numpy as np


# Change this path if your installation is different

pytesseract.pytesseract.tesseract_cmd = "tesseract"


def preprocess_image(image_path):

    """
    Improve receipt image quality
    before OCR
    """

    image = cv2.imread(
        image_path
    )


    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # Remove noise

    gray = cv2.threshold(
        gray,
        150,
        255,
        cv2.THRESH_BINARY
    )[1]


    return gray




def read_receipt(image_path):

    """
    Read receipt image and return text
    """

    processed_image = preprocess_image(
        image_path
    )

    text = pytesseract.image_to_string(
    processed_image,
    lang="eng+fra"
)


    return text.strip()
