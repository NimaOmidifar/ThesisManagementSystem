from src.main.FileManager import FileManager


class LoginAndChangePass:

    def __init__(self, user_id):
        self.user_id = user_id

    def master_login(self, password):
        file_obj = FileManager("../resources/data/Masters.json")
        user_list = file_obj.file_reader()

        for user in user_list:
            if user["id"] == self.user_id:
                if user["password"] == password:
                    return True

                return False

        return False

    def student_login(self, password):
        file_obj = FileManager("../resources/data/Students.json")
        user_list = file_obj.file_reader()

        for user in user_list:
            if user["id"] == self.user_id:
                if user["password"] == password:
                    return True

                return False

        return False

    def master_change_password(self, new_password):
        file_obj = FileManager("../resources/data/Masters.json")
        user_list = file_obj.file_reader()

        for user in user_list:
            if user["id"] == self.user_id:
                user["password"] = new_password
                print("Successfully changed password.")

        file_obj.file_writer(user_list)

    def student_change_password(self, new_password):
        file_obj = FileManager("../resources/data/Students.json")
        user_list = file_obj.file_reader()

        for user in user_list:
            if user["id"] == self.user_id:
                user["password"] = new_password
                print("Successfully changed password.")

        file_obj.file_writer(user_list)