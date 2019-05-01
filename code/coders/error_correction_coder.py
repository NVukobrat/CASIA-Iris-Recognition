from IrisRecognitionCasia.ReedSolomonCode.reedsolo import RSCodec


class ErrorCorrectionCoder:

    __reed_solomon_coder = RSCodec(100)

    @staticmethod
    def rs_encode(binary_key):
        """
        Encodes iris key with Reed Solomon Error Correction Codes. This codes
        enables iris to different from another iris sample from same person.
        This method can correct noise from different iris image of same person.

        :param binary_key: Iris binary key.
        :return: ECC encoded key.
        """
        encoded = ErrorCorrectionCoder.__reed_solomon_coder.encode(binary_key)

        return encoded

    @staticmethod
    def rs_decode(binary_key):
        """
        Decodes iris key with Reed Solomon Error Correction Codes. This codes
        enables iris to different from another iris sample from same person.
        This method can correct noise from different iris image of same person.

        :param binary_key: Iris binary ECC encoded key.
        :return: ECC encoded key
        """
        decoded = None

        try:
            decoded = ErrorCorrectionCoder.__reed_solomon_coder.decode(binary_key)
        except Exception as e:
            print("Invalid user: " + str(e))
            pass

        return decoded
