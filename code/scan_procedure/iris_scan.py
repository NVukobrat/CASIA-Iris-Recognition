from IrisRecognitionCasia.code.scan_procedure.Iris_normalizer import IrisNormalizer
from IrisRecognitionCasia.code.scan_procedure.feature_extractor import FeatureExtractor
from IrisRecognitionCasia.code.image_utils.image_utils import ImageUtils
from IrisRecognitionCasia.code.scan_procedure.iris_extractor import IrisExtractor
from IrisRecognitionCasia.code.scan_procedure.pupil_extractor import PupilExtractor


class IrisScan:
    @staticmethod
    def scan_iris(eye_image_path):
        """
        Eye
        """
        eye_image = ImageUtils.read_image(eye_image_path)

        """
        Pupil
        """
        pupil_detected, pupil_center, pupil_radius = PupilExtractor.extract(eye_image)
        if not ImageUtils.correct_image(pupil_detected):
            return None

        """
        Iris
        """
        iris_detected, iris_center, iris_radius = IrisExtractor.extract(pupil_detected, pupil_center)
        if not ImageUtils.correct_image(iris_detected):
            return None
        # ImageUtils.display_image(iris_detected, "Iris")

        """
        Normalized
        """
        normalized_iris = IrisNormalizer.normalize(iris_detected, iris_center, iris_radius, pupil_center, pupil_radius)
        if not ImageUtils.correct_image(normalized_iris):
            return None
        # ImageUtils.display_image(normalized_iris, "Normalized")

        """
        Extracted features
        """
        iris_features_binary = FeatureExtractor.extract_features(normalized_iris)
        # print("Features key {0}".format(np.shape(iris_features_binary)))
        # print(iris_features_binary)

        return iris_features_binary
