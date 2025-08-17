import json
import os
import shutil


class FileManager:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        try:
            with open(self.path, "r") as file:
                users = json.load(file)
                return users
        except FileNotFoundError:
            print(f"File not found.")
            return []

    def file_writer(self, users):
        try:
            with open(self.path, "w") as file:
                json.dump(users, file)
                print(f"File saved.")
        except FileNotFoundError:
            print(f"File not found.")

    def save_thesis(self, user_pdf_path, pdf_name, user_first_page_path, user_first_page_name, user_last_page_path, user_last_page_name):
        main_path = "../resources/data/theses"

        shutil.copy(user_pdf_path, f"{main_path}/{pdf_name}")
        shutil.copy(user_first_page_path, f"{main_path}/{user_first_page_name}")
        shutil.copy(user_last_page_path, f"{main_path}/{user_last_page_name}")

    def open_file(self):
        path = os.path.join("..", "resources", "data", "theses", self.path)
        os.startfile(path)
        try:
            os.startfile(self.path)
        except Exception as e:
            print(e)

    def delete_file(self):
        path = os.path.join("..", "resources", "data", "theses", self.path)
        os.remove(path)