import os


class FileUtil:

    @staticmethod
    def get_files_in_dir(path):
        file_names = os.listdir(path)

        files = []

        for file_name in file_names:
            files.append(os.path.join(path, file_name))

        return files
