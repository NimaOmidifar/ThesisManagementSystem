from doctest import master

from src.main.FileManager import FileManager


class Master:
    def __init__(self, master_id, password):
        self.master_id = int(master_id)
        self.password = password

    def thesis_decision(self, requester_id, decision = True):
        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        request_list = None
        for master in master_list:
            if master["id"] == self.master_id:
                request_list = master["thesis_requests"]
                index = 0
                for request in request_list:
                    if request["requester_id"] == requester_id:
                        master["thesis_requests"].remove(master["thesis_requests"][index])

                        student_obj = FileManager("../resources/data/Students.json")
                        student_list = student_obj.file_reader()
                        for student in student_list:
                            if student["id"] == requester_id:
                                if decision:
                                    student["thesis_request"]["status"] = "accepted"
                                else:
                                    student["thesis_request"]["status"] = "rejected"

                                    master["capacity"]["advisor"] = master["capacity"]["advisor"] + 1

                                    course_obj = FileManager("../resources/data/Courses.json")
                                    course_list = course_obj.file_reader()
                                    for course in course_list:
                                        if course["id"] == student["thesis_request"]["course_id"]:
                                            course["capacity"] = course["capacity"] + 1
                                            course_obj.file_writer(course_list)
                                            break

                                student_obj.file_writer(student_list)
                                break
                        break
                    index += 1
                master_obj.file_writer(master_list)






    def thesis_requests_print(self):
        student_name = ""
        request_date = ""
        course_title = ""

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
                            student_name = student["name"]
                            request_date = student["thesis_request"]["date"]

                            course_obj = FileManager("../resources/data/Courses.json")
                            course_list = course_obj.file_reader()
                            for course in course_list:
                                if course["id"] == student["thesis_request"]["course_id"]:
                                    course_title = course["title"]
                                    break
                            break

        if student_name:
            print(f"student name: {student_name}\ncourse title: {course_title}\nrequest date: {request_date}")
            print("------------------------------------")

