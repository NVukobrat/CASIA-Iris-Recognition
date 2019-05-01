import numpy as np
import cv2


class FeatureExtractor:

    __current_iris_binary = None

    @staticmethod
    def extract_features(normalized_iris):
        """
        Extract iris features using bank of Gabor filters. Then from
        filtered iris image extract binary code for further processing.

        :param normalized_iris: Normalized iris image.
        :return: Binary iris array.
        """
        filtered_iris = FeatureExtractor.__filter_image(normalized_iris)
        binary_code = FeatureExtractor.__extract_binary(filtered_iris)

        return binary_code

    @staticmethod
    def __filter_image(normalized_iris):
        """
        Extracts features from normalized iris using gabor filters. Tries to
        extract features with all filters and then returns best one.

        :param normalized_iris: Normalized iris image.
        :return: Extracted features.
        """
        filters = FeatureExtractor.__generate_gabor_bank()
        best_extraction = np.zeros_like(normalized_iris)

        for gabor_kernel in filters:
            filtered_image = cv2.filter2D(normalized_iris, cv2.CV_8UC3, gabor_kernel)
            np.maximum(best_extraction, filtered_image, best_extraction)

        return best_extraction

    @staticmethod
    def __generate_gabor_bank():
        """
        Generates Gabor filter bank.

        :return: Bank of gabor filters.
        """
        filters = []
        kernel_size = 31

        for theta in np.arange(0, np.pi, np.pi / 16):
            kern = cv2.getGaborKernel((kernel_size, kernel_size), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
            kern /= 1.5 * kern.sum()
            filters.append(kern)

        return filters

    @staticmethod
    def __extract_binary(filtered_iris):
        """
        Extracts binary iris template from filtered iris.

        :param filtered_iris: Filtered iris with Gabor filter.
        :return: Binary iris template.
        """
        binary_code = filtered_iris.astype(np.int).flatten()

        FeatureExtractor.__current_iris_binary = binary_code
        binary_string = ''.join(str(e) for e in binary_code)

        return binary_string
