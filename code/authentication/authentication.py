import numpy as np

from IrisRecognitionCasia.code.coders.error_correction_coder import ErrorCorrectionCoder
from IrisRecognitionCasia.code.coders.iris_coder import IrisCoder
from IrisRecognitionCasia.code.database.database import Database


class Authentication:
    """
    For precision test.
    """
    all_user_data = Database.select_all_user_data()
    FA = 0
    FR = 0
    ALL_IMPOSTOR = 1
    ALL_GENUINE = 1
    USER_PASS = 0

    @staticmethod
    def authenticate(iris_features_binary, user_id):
        """
        Get user data
        """
        all_user_data = Database.select_user_data(user_id)

        for user_dictionary in Authentication.all_user_data:
            private_key = user_dictionary['private_key']
            encrypted_iris_binary = user_dictionary['encrypted_biometrics']

            """
            Decrypting
            """
            decrypted_iris_binary = IrisCoder.decrypt_stored_key(iris_features_binary, encrypted_iris_binary)
            # print("Decrypted key {0}".format(len(decrypted_iris_binary)))
            # print(decrypted_iris_binary)

            """
            Check matching
            """
            if IrisCoder.iris_match(private_key, decrypted_iris_binary):
                # print("Successfully authenticate user {0} with {1} user biometrics.".format(user_id, user_dictionary['user_id']))
                if int(user_id) != int(user_dictionary['user_id']):
                    Authentication.FA += 1

            else:
                # print("Failed authentication for user {0} with {1} user biometrics.".format(user_id, user_dictionary['user_id']))
                if int(user_id) == int(user_dictionary['user_id']):
                    Authentication.FR += 1

            if int(user_id) == int(user_dictionary['user_id']):
                Authentication.ALL_GENUINE += 1

            if int(user_id) != int(user_dictionary['user_id']):
                Authentication.ALL_IMPOSTOR += 1

        Authentication.USER_PASS += 1

        print("One circle FAR: {0:f}".format(Authentication.FA / Authentication.ALL_IMPOSTOR))
        print("One circle FRR: {0:f}".format(Authentication.FR / Authentication.ALL_GENUINE))
        print(Authentication.FA, Authentication.FR, Authentication.ALL_IMPOSTOR, Authentication.ALL_GENUINE)
        print("Pass user: {0:d}".format(Authentication.USER_PASS))
        print("\n")
