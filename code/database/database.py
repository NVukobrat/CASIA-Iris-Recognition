import mysql.connector

from IrisRecognitionCasia.code.coders.iris_coder import IrisCoder


class Database:
    """
    Connection parameters.
    """
    connection = mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='casia_iris'
    )

    @staticmethod
    def insert_user_data(user_data):
        """
        Insert user data into database.

        :param user_data: User id and private key.
        """
        cursor = Database.connection.cursor()

        query = ("INSERT INTO users_data "
                 "(user_id, private_key) "
                 "VALUES (%(user_id)s, %(private_key)s)")

        cursor.execute(query, user_data)

        Database.connection.commit()

    @staticmethod
    def insert_user_biometrics(user_biometrics):
        """
        Insert user biometrics into database.

        :param user_biometrics: User biometrics.
        """
        cursor = Database.connection.cursor()

        query = ("INSERT INTO users_biometrics "
                 "(user_id, encrypted_biometrics) "
                 "VALUES (%(user_id)s, %(encrypted_biometrics)s)")

        cursor.execute(query, user_biometrics)

        Database.connection.commit()

    @staticmethod
    def select_user_data(user_id):
        """
        Select user for certain user id.

        :param user_id: User id.
        :return: List with user data.
        """
        user_data_list = []
        user_data_template = {}

        cursor = Database.connection.cursor()

        query = ("SELECT users_data.user_id, private_key, encrypted_biometrics "
                 "FROM users_data "
                 "INNER JOIN users_biometrics "
                 "ON users_data.user_id = users_biometrics.user_id "
                 "WHERE users_data.user_id = " + str(user_id))

        cursor.execute(query)

        for user_id, private_key, encrypted_biometrics in cursor:
            user_data_template['user_id'] = user_id
            user_data_template['private_key'] = private_key
            user_data_template['encrypted_biometrics'] = encrypted_biometrics

            user_data_list.append(user_data_template.copy())

            user_data_template.clear()

        return user_data_list

    @staticmethod
    def select_all_user_data():
        """
        Select all users data.
        """
        user_data_list = []
        user_data_template = {}

        cursor = Database.connection.cursor()

        query = ("SELECT users_data.user_id, private_key, encrypted_biometrics "
                 "FROM users_data "
                 "INNER JOIN users_biometrics "
                 "ON users_data.user_id = users_biometrics.user_id ")

        cursor.execute(query)

        for user_id, private_key, encrypted_biometrics in cursor:
            user_data_template['user_id'] = user_id
            user_data_template['private_key'] = private_key
            user_data_template['encrypted_biometrics'] = encrypted_biometrics

            user_data_list.append(user_data_template.copy())

            user_data_template.clear()

        return user_data_list