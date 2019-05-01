import cv2
import math


class PupilExtractor:

    current_pupil_center = (0, 0)
    current_pupil_radius = 0

    @staticmethod
    def extract(eye_image):
        """
        Process eye image. Removes pupil noise, finds pupil boundaries
        and pupil center of eye image.

        :param eye_image: Original eye image.
        :return: Processes eye image and Coordinates of current processed pupil.
        """
        contours = PupilExtractor.__extract_contours(eye_image)
        suitable_contours = PupilExtractor.__parse_contours(contours)
        eye_image = PupilExtractor.__process_pupil(eye_image, suitable_contours)

        return eye_image, PupilExtractor.current_pupil_center, PupilExtractor.current_pupil_radius

    @staticmethod
    def __extract_contours(eye_image):
        """
        Extracts contours of image. For better accuracy firstly threshold
        is applied. Then contours are extracted using Open CV library.

        Function for extracting contours uses 3 parameters. First is image,
        in our case it is threshold image. Second parameter RETR_LIST specifies
        that function retrieves all contours without creating any parent-child
        relationship. Third parameter CHAIN_APPROX_NONE specifies that all boundary
        points needs to be returned.

        :param eye_image: Original image of eye.
        :return: Contours find in eye image.
        """
        thresh = cv2.inRange(eye_image, 0, 120)
        thresh, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        return contours

    @staticmethod
    def __parse_contours(contours):
        """
        Loops over all contours and chose most suitable
        for fitting pupil.

        :param contours: All extracted contours.
        :return: List of most suitable contours.
        """
        most_suitable_contours = []
        for contour in contours:

            if PupilExtractor.__inadequate_contour(contour):
                continue

            most_suitable_contours.append(contour)

        return most_suitable_contours

    @staticmethod
    def __inadequate_contour(contour):
        """
        Checks contour area and circularity. If one of features
        are not satisfied contour is ignored from rest of
        processing.

        :param contour: Current contour.
        :return: Boolean relative on feature satisfaction.
        """
        area = cv2.contourArea(contour)

        if area < 500:
            return True

        circumference = cv2.arcLength(contour, True)
        circularity = circumference ** 2 / (4 * math.pi * area)

        if circularity > 2.2:
            return True

        return False

    @staticmethod
    def __process_pupil(eye_image, contours):
        """
        Process original eye image. Fills eye pupil with black ellipse
        in order to remove pupil noise. Also marks center of pupil.

        :param eye_image: Original eye image.
        :param contours: Suitable pupil contours.
        :return: None if there is no contours or processed eye image.
        """
        if len(contours) == 0:
            return None

        for contour in contours:
            PupilExtractor.__fill_eye_pupil(eye_image, contour)
            PupilExtractor.__fill_pupil_center(eye_image, contour)

        return eye_image

    @staticmethod
    def __fill_eye_pupil(eye_image, contour):
        """
        Fills eye pupil with ellipse. First creates ellipse based
        on extracted contour and then draws that ellipse over eye pupil.

        :param eye_image: Original eye image.
        :param contour: Pupil contour.
        """
        try:
            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(eye_image, box=ellipse, color=(0, 255, 0), thickness=cv2.FILLED)
        except:
            pass

    @staticmethod
    def __fill_pupil_center(eye_image, contour):
        """
        Draws center of pupil with white circle. First gets all moments
        from contour. Then calculates center of contour and draws it on
        original eye image. Also saves coordinates of pupil center to
        static variable of class.

        :param eye_image: Original eye image.
        :param contour: Pupil contour.
        """
        moments = cv2.moments(contour)
        if moments['m00'] != 0:
            center = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))
            cv2.circle(eye_image, center, 3, (0, 255, 0), cv2.FILLED)

            PupilExtractor.current_pupil_center = center
            PupilExtractor.current_pupil_radius = PupilExtractor.__get_pupil_radius(moments['m00'])

    @staticmethod
    def __get_pupil_radius(pupil_area):
        """
        Calculate radius of pupil circle.

        :param pupil_area:
        :return:
        """
        return int(math.sqrt(pupil_area / math.pi))
