import random
import string

import bitarray


class KeyGenerator:

    encoded_key_length = 0

    @staticmethod
    def generate_private_key(key_length=254):
        """
        Generates private binary key iris encryption. Private key should be
        the same length as extracted iris template because of XORing operation.

        :param key_length: Length of key.
        :return: Private key.
        """
        random_generated_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=key_length))

        return random_generated_key

    @staticmethod
    def to_binary_from_bytearray(random_generated_key):
        binary_key = bin(int.from_bytes(random_generated_key, byteorder="big")).strip('0b')

        if KeyGenerator.encoded_key_length == 0:
            KeyGenerator.encoded_key_length = len(binary_key)

        if len(binary_key) != KeyGenerator.encoded_key_length:
            difference = KeyGenerator.encoded_key_length - len(binary_key)
            if difference < 0:
                binary_key = binary_key[:difference]
            else:
                binary_key = binary_key + ('0' * difference)

        return binary_key

    @staticmethod
    def to_bits_from_string(s):
        result = []
        for c in s:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])

        string_key = ''.join(str(i) for i in result)

        return string_key

    @staticmethod
    def from_bits_to_string(bits):
        chars = []
        for b in range(len(bits) / 8):
            byte = bits[b * 8:(b + 1) * 8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

        return ''.join(chars)
