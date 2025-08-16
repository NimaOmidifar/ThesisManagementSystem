from datetime import datetime
from doctest import master

from src.main.FileManager import FileManager


class Master:
    def __init__(self, master_id, password):
        self.master_id = int(master_id)
        self.password = password

    def thesis_decision(self, requester_id, decision = True):
        requester_id = int(requester_id)
        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        request_list = None
        for master in master_list:
            if master["id"] == self.master_id:
                request_list = master["thesis_requests"]
                for index, request in enumerate(request_list):
                    print(request["requester_id"])
                    print(requester_id)
                    if request["requester_id"] == requester_id:
                        print(2)
                        master["thesis_requests"].remove(master["thesis_requests"][index])

                        student_obj = FileManager("../resources/data/Students.json")
                        student_list = student_obj.file_reader()
                        for student in student_list:
                            if student["id"] == requester_id:
                                print(3)
                                if decision:
                                    print(4)
                                    student["thesis_request"]["status"] = "accepted"
                                    student_obj.file_writer(student_list)
                                    master_obj.file_writer(master_list)
                                    return "The student was accepted."
                                else:
                                    print(5)
                                    student["thesis_request"]["status"] = "rejected"

                                    master["capacity"]["advisor"] = master["capacity"]["advisor"] + 1

                                    course_obj = FileManager("../resources/data/Courses.json")
                                    course_list = course_obj.file_reader()
                                    for course in course_list:
                                        if course["id"] == student["thesis_request"]["course_id"]:
                                            print(6)
                                            course["capacity"] = course["capacity"] + 1
                                            course_obj.file_writer(course_list)
                                            student_obj.file_writer(student_list)
                                            master_obj.file_writer(master_list)
                                            return "The student was rejected."
                return "There is no student with that ID."



    def thesis_defense_decision(self, requester_id, decision = True, ):
        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        print("1")
        for master in master_list:
            if master["id"] == self.master_id:
                print("2")
                request_list = master["defense_requests"]
                index = 0
                for request in request_list:
                    if request["requester_id"] == requester_id:
                        print("3")
                        student_obj = FileManager("../resources/data/Students.json")
                        student_list = student_obj.file_reader()
                        for student in student_list:
                            if student["id"] == requester_id:
                                print("4")
                                if decision:
                                    student["defense_request"]["status"] = "accepted"
                                    print("5")


                                else:
                                    print("6")
                                    student["defense_request"]["status"] = "rejected"

                                    defense_obj = FileManager("../resources/data/Defenses.json")
                                    defense_list = defense_obj.file_reader()
                                    defense_list_copy = defense_list.copy()
                                    defense_index = 0
                                    for defense in defense_list_copy:
                                        if defense["id"] == master["defense_requests"][index]["defense_id"]:
                                            defense_list.remove(defense_list[defense_index])
                                            break
                                        defense_index += 1

                                    master["defense_requests"].remove(master["defense_requests"][index])
                                    master_obj.file_writer(master_list)

                                    defense_obj.file_writer(defense_list)
                                student_obj.file_writer(student_list)

                index += 1

    def choose_examiner(self, internal_examiner, external_examiner, date):
        defense_date = datetime.strptime(date, "%d/%m/%Y").date()
        now = datetime.now().date()

        if defense_date > now:
            master_obj = FileManager("../resources/data/Masters.json")
            master_list = master_obj.file_reader()
            for master in master_list:
                if master["name"] == internal_examiner:
                    if master["capacity"]["examiner"] != 0:
                        master["capacity"]["examiner"] = master["capacity"]["examiner"] - 1

                        dic = {

                        }

                    else:
                        print("The internal master is busy.")
                else:
                    print("There is no such internal master.")

        else:
            print("Invalid date.")

    def thesis_requests_print(self):
        student_id = ""
        student_name = ""
        request_date = ""
        course_title = ""
        final_list = []

        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        for master in master_list:
            if master["id"] == self.master_id:
                if not master["thesis_requests"]:
                    break

                student_obj = FileManager("../resources/data/Students.json")
                student_list = student_obj.file_reader()

                for request in master["thesis_requests"]:
                    for student in student_list:
                        if student["id"] == request["requester_id"]:
                            student_id = student["id"]
                            student_name = student["name"]
                            request_date = student["thesis_request"]["date"]

                            course_obj = FileManager("../resources/data/Courses.json")
                            course_list = course_obj.file_reader()
                            for course in course_list:
                                if course["id"] == student["thesis_request"]["course_id"]:
                                    course_title = course["title"]
                                    sub_tuple = (request_date, course_title, student_name, student_id)
                                    final_list.append(sub_tuple)
                                    break
                            break

        if student_name:
            return final_list

    def thesis_defense_requests_print(self):
        student_id = ""
        student_name = ""
        title = ""
        abstract = ""
        keywords = None
        pdf_path = ""
        first_page_path = ""
        last_page_path = ""
        date = ""
        final_list = []

        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        for master in master_list:
            if master["id"] == self.master_id:
                if not master["defense_requests"]:
                    return final_list

            defense_obj = FileManager("../resources/data/Defenses.json")
            defense_list = defense_obj.file_reader()
            for request in master["defense_requests"]:
                for defense in defense_list:
                    if defense["id"] == request["defense_id"]:
                        student_id = defense["student_id"]
                        student_name = defense["student_name"]
                        title = defense["title"]
                        abstract = defense["abstract"]
                        keywords = defense["keywords"]
                        pdf_path = defense["pdf_name"]
                        first_page_path = defense["first_page_name"]
                        last_page_path = defense["last_page_name"]
                        date = defense["date"]
                        sub_tuple = (student_id, student_name, title, abstract, keywords, pdf_path, first_page_path, last_page_path, date)
                        final_list.append(sub_tuple)

                        return final_list