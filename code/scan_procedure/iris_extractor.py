import cv2
import numpy as np


class IrisExtractor:

    current_iris_center = (0, 0)
    current_iris_radius = 0

    @staticmethod
    def extract(eye_image, pupil_center):
        preprocessed_image = IrisExtractor.__preprocess_image(eye_image)
        closest_circle = IrisExtractor.__detect_iris(preprocessed_image, pupil_center)
        iris_image = IrisExtractor.__process_iris(eye_image, closest_circle)

        return iris_image, IrisExtractor.current_iris_center, IrisExtractor.current_iris_radius

    @staticmethod
    def __preprocess_image(eye_image):
        """
        Applies all filter and prepares image for further processing.
        First Gaussian Blur is applied to reduce image details, for better
        contour defining. Second, Canny filter is applied for purpose
        of precise contour finding.

        :param eye_image: Iris image with filled pupil.
        :return: Pre processed eye image.
        """
        copy_of_image = eye_image.copy()
        preprocessed_image = cv2.GaussianBlur(copy_of_image, (9, 9), 0)
        preprocessed_image = cv2.Canny(preprocessed_image, 10, 30, 10)

        return preprocessed_image

    @staticmethod
    def __detect_iris(preprocessed_image, pupil_center):
        """
        Detects and marks Iris in eye image. Uses Hough Circles to determinate the
        possible iris position. OpenCV 3 has HoughCircle function that uses
        Hough gradient method, which is made up of two main stages. The first stage
        involves edge detection and finding the possible circle centers
        and the second stage finds the best radius for each candidate center.

        After circle detection function parses all circles and finds best fit
        by comparing centers of circles with center of eye pupil.

        :param preprocessed_image: Preprocessed eye image.
        :param pupil_center: Coordinates of pupil.
        :return: Best circle fit.
        """
        circles = cv2.HoughCircles(preprocessed_image, cv2.HOUGH_GRADIENT, 1, 10, param1=70, param2=20, minRadius=100, maxRadius=0)
        if circles is None:
            return None
        circles = np.uint16(np.around(circles))
        closest_circle = IrisExtractor.__closest_to_pupil_center(circles[0, :], pupil_center)

        IrisExtractor.current_iris_center = (closest_circle[0], closest_circle[1])
        IrisExtractor.current_iris_radius = closest_circle[2]

        return closest_circle

    @staticmethod
    def __process_iris(eye_image, iris_circle):
        """
        Crops the iris image from eye image. Creates mask with iris circle that
        was previously detected. And then & (and's) eye image with iris circle mask
        to crop just the iris image from eye image.

        :param eye_image:
        :param iris_circle:
        :return:
        """
        copy_of_image = eye_image.copy()
        x, y, r = iris_circle
        mask = np.zeros(copy_of_image.shape, dtype=np.uint8)
        cv2.circle(mask, (x, y), r, (255, 255, 255), -1, 8, 0)

        iris_image = copy_of_image & mask
        iris_image = iris_image[(y - r):(y + r), (x - r):(x + r)]

        return iris_image

    @staticmethod
    def __closest_to_pupil_center(circles, pupil_center):
        """
        Calculates the closest center of Iris circle to center of pupil circle.
        To calculate the difference between two center, this function uses
        Euclidean distance.

        :param circles: All founded circles on Iris.
        :param pupil_center: Coordinates of iris pupil.
        :return: Closest match iris circle center to pupil center.
        """
        closest_circle = (0, 0, 0)
        min_distance = -1

        for circle in circles:
            x, y, r = circle

            distance = np.math.sqrt(((pupil_center[0] - x) ** 2) + ((pupil_center[1] - y) ** 2))

            if min_distance < 0 or distance < min_distance:
                min_distance = distance
                closest_circle = circle

        return closest_circle
