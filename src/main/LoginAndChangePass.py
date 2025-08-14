from src.main.FileManager import FileManager


class LoginAndChangePass:

    def __init__(self, user_id):
        self.user_id = int(user_id)

    def login(self, password, user = "student"):
        global name
        file_obj = None
        if user == "student":
            file_obj = FileManager("../resources/data/Students.json")
        elif user == "master":
            file_obj = FileManager("../resources/data/Masters.json")
        user_list = file_obj.file_reader()

        for users in user_list:
            if users["id"] == self.user_id:
                if users["password"] == password:
                    name = users["name"]
                    return True

                return False

        return False


    def change_password(self, new_password, user = "student"):
        file_obj = None
        if user == "student":
            file_obj = FileManager("../resources/data/Students.json")
        elif user == "master":
            file_obj = FileManager("../resources/data/Masters.json")
        user_list = file_obj.file_reader()

        for users in user_list:
            if users["id"] == self.user_id:
                users["password"] = new_password
                file_obj.file_writer(user_list)
                return True

        return False

    def get_name(self):
        return name