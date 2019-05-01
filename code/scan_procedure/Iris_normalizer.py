import cv2
import numpy as np

from IrisRecognitionCasia.code.image_utils.image_utils import ImageUtils


class IrisNormalizer:
    @staticmethod
    def normalize(iris_detected, iris_center, iris_radius, pupil_center, pupil_radius):
        """
        Normalizes iris image. Converts polar iris coordinates to
        cartesian coordinates.

        :return: Normalized iris image.
        """
        iris_float = iris_detected.copy().astype(np.float64)
        x, y = iris_float.shape
        x_cart = ((x / 2.0) ** 2)
        y_cart = ((y / 2.0) ** 2)
        area = np.sqrt(x_cart + y_cart)

        normalized = cv2.linearPolar(iris_float, (x / 2, y / 2), area, cv2.WARP_FILL_OUTLIERS)
        normalized = normalized / 255
        normalized = normalized[0:, int(normalized.shape[1] * 0.2):int(normalized.shape[1] * 0.67)]
        normalized = np.rot90(normalized, 3)
        normalized = cv2.resize(normalized, (180, 50))

        return normalized
