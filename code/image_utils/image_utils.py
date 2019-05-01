import cv2
import numpy as np


class ImageUtils:

    @staticmethod
    def read_image(image_path):
        """
        Reads image from image path in gray scale.

        :param image_path: Path to image.
        :return: Image.
        """
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        return image

    @staticmethod
    def display_image(image, window_name):
        """
        Displays image on predefined interval.

        :param image: Image.
        :param window_name: Name of window for displaying.
        """
        if image is not None and np.any(image <= 0):
            cv2.imshow(window_name, image)
            cv2.waitKey(10)

    @staticmethod
    def correct_image(image):
        if image is None:
            return False

        if not np.any(image <= 0):
            return False

        return True
