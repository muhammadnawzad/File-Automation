#!/usr/bin/env python

import os
import time
import os.path
from random import randint
from ExtraInfo import types, locations, docs, working_directories


class FileOrganizer:

    def __init__(self, directory_path):
        self.directory_path = directory_path

    def path_maker(self, root, file_name):
        """(str, str) -> str

        Returns a string containing the full path of a file,
        from root of the file and its name.

        >>> path_maker("/home/hama/Downloads", "area.cpp")
        "/home/hama/Downloads/area.cpp"
        >>> path_maker("/home/hama/Downloads/", "FuzzBuzz.py")
        "/home/hama/Downloads/FuzzBuzz.py"
        """

        return os.path.join(root, file_name)

    def extention_finder(self, path):
        """(str) -> str

        Takes in a string of full path of a file. If exists,
        returns a string of its extention, else returns False.

        >>> extention_finder("/home/hama/Downloads/area.cpp")
        ".cpp"
        >>> extention_finder("/home/hama/Downloads/FuzzBuzz.py")
        ".py"
        """

        if os.path.exists(path):
            if os.path.isfile(path):
                return os.path.splitext(path)[1]
        return False

    def category_selector(self, extention):
        """(str) -> str

        Takes in a string of an extention of a file. If not False,
        returns the category of the extention, else returns False.

        Precondition: The extention must be in one of the categories.

        >>> category_selector(".cpp")
        "programming-files"
        >>> category_selector(".mp4")
        "video"
        """

        if extention != False:
            for category in types:
                if extention in types[category]:
                    return category
                    break
            return False

    def get_prefix(self, path):
        """(str) -> str

        Takes in a string of full path of a file. If it is one of the doc
        categories returns the first 3 characters of name of the file, else 2.

        Precondition: A prefix of a specific directory should be provided
        at the begining of the name of the file.

        >>> get_prefix("/home/hama/Downloads/umaMath-week11.pdf")
        "uma"
        >>> get_prefix("/home/hama/Downloads/pyFuzzBuzz.py")
        "py"
        """

        prefix = os.path.basename(path)
        if self.category_selector(self.extention_finder(path)) not in docs:
            return prefix[:2]
        else:
            return prefix[:3]

    def get_original_name(self, path):
        """(str) -> str

        Takes in a string of full path of a file. returns a string of
        the original file name without any prefix.

        Precondition: A prefix of a specific directory should be provided
        at the begining of the name of the file.

        >>> get_original_name("/home/hama/Downloads/umaMath-week11.pdf")
        "Math-week11.pdf"
        >>> get_original_name("/home/hama/Downloads/pyFuzzBuzz.py")
        "FuzzBuzz.py"
        """

        file_name = os.path.basename(path)
        if self.category_selector(self.extention_finder(path)) not in docs:
            return file_name[2:]
        else:
            return file_name[3:]

    def random_name_generator(self, path):
        """(str) -> str

        Takes in a string of full path of a file. Generates a random
        integer at the end of the name of the file, the returns the new name.

        >>> random_name_generator("/home/hama/Downloads/umaMath-week11.pdf")
        "Math-week11.pdf"
        >>> random_name_generator("/home/hama/Downloads/pyFuzzBuzz.py")
        "FuzzBuzz.py"
        """

        file_name = os.path.splitext(path)[0]
        extention = os.path.splitext(path)[1]
        return f"""{file_name}-{randint(1, 250) % randint(1, 250)}{extention}"""

    def copy(self, file_source, destination_root):
        """(str, str) -> str

        Returns a string containing the full path of the newly moved file,
        from a full path of a file and root of the destination.

        Note: If the a file with the same name already exists, a new name will be generated.

        >>> copy("/home/hama/Downloads/area.cpp", "/home/hama/Codes/C++/")
        "/home/hama/Codes/C++/area.cpp"
        >>> copy("/home/hama/Downloads/FuzzBuzz.py", "/home/hama/Codes/Python/")
        "/home/hama/Codes/Python/FuzzBuzz.py"
        """

        if not os.path.exists(self.path_maker(destination_root, self.get_original_name(file_source))):
            file_name = os.path.basename(file_source)
            file_destination = self.path_maker(
                destination_root, self.get_original_name(file_source))
            os.system(f"cp -pa {file_source} {file_destination}")
            return file_destination
        else:
            file_name = self.random_name_generator(self.path_maker(
                destination_root, self.get_original_name(file_source)))
            file_destination = self.path_maker(destination_root, file_name)
            os.system(f"cp -pa {file_source} {file_destination}")
            return file_destination


# Activated on these directories
paths = [FileOrganizer(f"{directory}") for directory in working_directories]
while True:
    for path in paths:
        # Get the files and directories in the root directory.
        for root, directories, files in os.walk(path.directory_path):
            root, directories, files = root, directories, files
            break

        # List the files in the directory
        list_of_files = []
        for file in files:
            list_of_files.append(path.path_maker(root, file))

        # Loop through the files and copy each one of them.
        proccess = True
        for file in list_of_files:
            if proccess:
                current_file = file

                file_category = path.category_selector(
                    path.extention_finder(current_file))
                if file_category in locations:
                    if locations[file_category].get(path.get_prefix(current_file)) != None:
                        destination_root = locations[file_category].get(
                            path.get_prefix(current_file))

                        # Check if there is a whitespace in the path, cause it cause infinite loop.
                        if not (" " in current_file):
                            new_file_destination = path.copy(
                                current_file, destination_root)
                        else:
                            continue
                        if os.path.exists(new_file_destination):
                            os.remove(current_file)

                        # Check if the file is moved and the proccess is done, otherwise wait until it is done.
                        if not os.path.exists(current_file) and os.path.exists(new_file_destination):
                            proccess = True
                        else:
                            proccess = False
                            while not proccess:
                                if not os.path.exists(current_file) and os.path.exists(new_file_destination):
                                    proccess = True
                                else:
                                    proccess = False
                                time.sleep(10)

        time.sleep(5)

    time.sleep(30)
    
# By: Muhammad Nawzad Abdullah
# Software Engineer to be.
