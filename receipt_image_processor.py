import cv2
import numpy as np


def preprocess_receipt(image_path):

    image = cv2.imread(image_path)


    if image is None:
        raise Exception(
            "Cannot read image"
        )


    # Convert to grayscale

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # Reduce noise

    blur = cv2.GaussianBlur(
        gray,
        (5,5),
        0
    )


    # Increase contrast

    threshold = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY +
        cv2.THRESH_OTSU
    )[1]


    # Save processed image

    output = "receipts/processed_receipt.jpg"


    cv2.imwrite(
        output,
        threshold
    )


    return output