import os


class ImageReader:

    def __init__(self, path):
        self.path = path
        self.images = {}

    def read_data(self):
        """
        Reads all images from CASIA root folder that is forwarded
        in constructor. Creates dictionary of folder names and images
        inside it as keys and values respectively.

        :return: Dataset dictionary.
        """
        for image_folder in os.listdir(self.path):
            self.images[image_folder] = []
            image_folder_path = self.path + os.sep + image_folder
            for left_right_folders in os.listdir(image_folder_path):
                left_right_folders_path = image_folder_path + os.sep + left_right_folders
                for image_name in os.listdir(left_right_folders_path):
                    absolute_images_path = left_right_folders_path + os.sep + image_name
                    self.images[image_folder].append(absolute_images_path)

        return self.images
