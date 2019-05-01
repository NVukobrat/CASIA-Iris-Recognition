import os


class IrisCoder:

    key_difference = 0

    @staticmethod
    def encrypt_iris(binary_iris, private_key):
        """
        Encrypts filtered iris template. First transforms iris template image
        to binary array. Then encrypts extracted iris template with private key.

        :param binary_iris: Extracted iris features.
        :param private_key: Private binary key.
        :return: Encrypted iris binary key.
        """
        if IrisCoder.key_difference == 0:
            difference = len(binary_iris) - len(private_key)
            if difference < 0:
                print("Private key is bigger then Binary Irs, correct this.")
            IrisCoder.key_difference = difference

            file = open('key_difference.txt', 'w')
            file.write(str(IrisCoder.key_difference))
            file.close()

        private_key = IrisCoder.__correct_bits_for_xor(binary_iris, private_key)

        if not IrisCoder.__suitable_keys(binary_iris, private_key):
            print("Unsuitable keys for encryption: Binary iris ({0}) don't match Binary key ({1})".format(
                len(binary_iris), len(private_key))
            )
            return None

        encrypted_iris_key = ''.join('0' if i == j else '1' for i, j in zip(binary_iris, private_key))

        return encrypted_iris_key

    @staticmethod
    def __correct_bits_for_xor(binary_iris, binary_key):
        """
        Correct iris binary key for xor operation. Because of RS Encoder imperfection
        some noise is created in this step.

        :param binary_iris: Binary iris code.
        :param binary_key: Binary key.
        """
        if len(binary_key) == 9000:
            return binary_key

        add_on = ('0' * IrisCoder.key_difference)
        binary_key = add_on + binary_key

        return binary_key

    @staticmethod
    def __suitable_keys(iris_key, private_key):
        """
        Checks if iris key and generated private key are suitable for
        encryption phase.

        :param iris_key: Extracted iris key.
        :param private_key: Generated private key.
        :return: True or False depending comparision results.
        """
        if len(iris_key) != len(private_key):
            return False

        return True

    @staticmethod
    def decrypt_stored_key(encrypted_iris, private_key):
        """
        Decrypts encrypted iris key with private key using XOR operation.

        :param encrypted_iris: Encrypted iris template.
        :param private_key: Generated private key for current iris template.
        :return: Decrypted iris template.
        """
        if not IrisCoder.__suitable_keys(encrypted_iris, private_key):
            print("Unsuitable keys for decryption: Binary iris ({0}) don't match Binary key ({1})".format(
                len(encrypted_iris), len(private_key))
            )
            return None

        decrypted_key = ''.join('0' if i == j else '1' for i, j in zip(encrypted_iris, private_key))

        decrypted_key = IrisCoder.__correct_bits_after_xor(decrypted_key)

        return decrypted_key

    @staticmethod
    def __correct_bits_after_xor(binary_key):
        """
        Pops needed bits for further processing. Number 190 is the number of
        added bits for XOR function.

        :param binary_key: Binary key.
        """
        if os.path.exists('key_difference.txt') and IrisCoder.key_difference == 0:
            file = open('key_difference.txt', 'r')
            IrisCoder.key_difference = int(file.read())
            file.close()

        binary_key = binary_key[IrisCoder.key_difference:]

        return binary_key

    @staticmethod
    def string_binary_to_list(binary):
        """
        Reforms stored binary string to binary list.

        :param binary: Binary string.
        :return: Binary list.
        """
        binary_list = []
        for char in binary.split(','):
            binary_list.append(int(char))

        return

    difference_sum = 0
    difference_num = 0
    @staticmethod
    def iris_match(extracted_key, private_key):
        distance = IrisCoder.__hamming_distance(extracted_key, private_key)
        difference = ((distance / len(private_key)) * 100)

        IrisCoder.difference_sum += difference
        IrisCoder.difference_num += 1

        if difference > 25:
            return False
        else:
            return True

    @staticmethod
    def __hamming_distance(extracted_key, private_key):
        if len(extracted_key) != len(private_key):
            print("Wrong key length for hamming: Extracted ({0}), Private ({1})".format(len(extracted_key), len(private_key)))
        return sum(c1 != c2 for c1, c2 in zip(extracted_key, private_key))

