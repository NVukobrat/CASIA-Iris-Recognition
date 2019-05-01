from IrisRecognitionCasia.code.coders.error_correction_coder import ErrorCorrectionCoder
from IrisRecognitionCasia.code.coders.iris_coder import IrisCoder
from IrisRecognitionCasia.code.database.database import Database
from IrisRecognitionCasia.code.enrolment_procedure.key_generator import KeyGenerator
import numpy as np


class Enrolment:
    @staticmethod
    def enroll(user_id, user_iris_keys):
        """
        Key generation
        """
        private_key = KeyGenerator.generate_private_key()
        # print("Private key {0}".format(len(private_key)))
        # print(private_key)

        """
        Key to binary
        """
        encoded_key = KeyGenerator.to_bits_from_string(private_key)
        # print("Binary private key ({0})".format(len(encoded_key)))
        # print(encoded_key)

        """
        Store user data
        """
        user_data = {
            'user_id': str(user_id),
            'private_key': str(encoded_key)[:]
        }

        Database.insert_user_data(user_data)
        # print(user_data)

        for iris_features_binary in user_iris_keys:
            """
            Encrypting
            """
            encrypted_iris_binary = IrisCoder.encrypt_iris(iris_features_binary, encoded_key)
            # print("Encrypted key {0}".format(len(encrypted_iris_binary)))
            # print(encrypted_iris_binary)

            """
            Store user biometrics
            """
            user_biometrics = {
                'user_id': str(user_id),
                'encrypted_biometrics': str(encrypted_iris_binary)
            }

            Database.insert_user_biometrics(user_biometrics)
            # print(user_biometrics)
