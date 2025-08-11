import json
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