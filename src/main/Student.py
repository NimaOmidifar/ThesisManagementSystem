from datetime import datetime
from doctest import master

from src.main.FileManager import FileManager
from src.main.LoginAndChangePass import LoginAndChangePass

class Student:
    def __init__(self, student_id, password):
        self.student_id = int(student_id)
        self.password = password

    def take_thesis(self, thesis_id):
        thesis_id = int(thesis_id)
        course_obj = FileManager("../resources/data/Courses.json")
        course_list = course_obj.file_reader()

        for course in course_list:
            if course["id"] == thesis_id:
                capacity = int(course["capacity"])
                if capacity != 0:
                    student_file = FileManager("../resources/data/Students.json")
                    student_list = student_file.file_reader()
                    request_date = None
                    for student in student_list:
                        if student["id"] == self.student_id:
                            if student["thesis_request"]["status"] in ["pending", "accepted"]:
                                print("You reserved an unit before.")
                                break

                            capacity -= 1
                            course["capacity"] = capacity
                            course_obj.file_writer(course_list)

                            request_date = datetime.now().strftime("%d/%m/%Y")
                            student["thesis_request"]["status"] = "pending"
                            student["thesis_request"]["date"] = request_date
                            student["thesis_request"]["course_id"] = course["id"]
                            student["thesis_request"]["master_id"] = course["master_id"]
                            student_file.file_writer(student_list)

                            master_file = FileManager("../resources/data/Masters.json")
                            master_list = master_file.file_reader()
                            for master in master_list:
                                if course["master_id"] == master["id"]:
                                    master["capacity"]["advisor"] -= 1
                                    master["thesis_requests"].append({"requester_id": self.student_id, "date": request_date})
                                    master_file.file_writer(master_list)
                                    break

                            print("The unit was successfully reserved.")
                            break
                else:
                    print("The course is full.")

                break

    def take_thesis_defense(self, title, abstract, keywords, pdf_path, first_page_path, last_page_path):
        student_obj = FileManager("../resources/data/Students.json")
        student_list = student_obj.file_reader()
        for student in student_list:
            if student["id"] == self.student_id:
                if student["defense_request"]["status"] == "no_request":
                    if student["thesis_request"]["status"] == "accepted":
                        request_date = datetime.strptime(student["thesis_request"]["date"], "%d/%m/%Y").date()
                        date_now = datetime.now().date()
                        date_now_str = datetime.now().strftime("%d/%m/%Y")
                        if (date_now - request_date).days >= 90:
                            defense_obj = FileManager("../resources/data/Defenses.json")
                            defense_list = defense_obj.file_reader()
                            if defense_list:
                                defense_id = defense_list[-1]["id"] + 1
                            else:
                                defense_id = 1
                            defense_dic = {
                                "id": defense_id,
                                "title": title,
                                "abstract": abstract,
                                "keywords": keywords,
                                "pdf_path": pdf_path,
                                "first_page_path": first_page_path,
                                "last_page_path": last_page_path,
                                "date": date_now_str
                            }
                            defense_list.append(defense_dic)
                            defense_obj.file_writer(defense_list)

                            student["defense_request"]["status"] = "pending"
                            student["defense_request"]["date"] = date_now_str
                            student["defense_request"]["defense_id"] = defense_id
                            student_obj.file_writer(student_list)

                            master_obj = FileManager("../resources/data/Masters.json")
                            master_list = master_obj.file_reader()
                            for master in master_list:
                                if master["id"] == student["thesis_request"]["master_id"]:
                                    master["defense_requests"].append({"requester_id": self.student_id, "date": date_now_str, "defense_id": defense_id})
                                    master_obj.file_writer(master_list)
                                    break

                        else:
                            print("Three months must have passed since the unit registration.")
                    else:
                        print("Wait for master decision.")
                else:
                    print("You reserved a thesis defense before.")

    def status_print(self):
        student_file = FileManager("../resources/data/Students.json")
        student_list = student_file.file_reader()
        for student in student_list:
            if student["id"] == self.student_id:
                print(f"date: {student['thesis_request']['date']}\nstatus: {student['thesis_request']['status']}")
                break

    def get_courses(self):
        course_obj = FileManager("../resources/data/Courses.json")
        course_list = course_obj.file_reader()
        return course_list
        # for course in course_list:
        #     print(f"id: {course['id']}\ntitle: {course['title']}\nmaster: {course['master']}\nyear: {course['year']}\nsemester: {course['semester']}\ncapacity: {course['capacity']}")
        #     for _ in course['resources']:
        #         print(_, end = ", ")
        #     print(f"\nsessions: {course['sessions']}\nunits: {course['units']}")
        #     print("-----------------------------------")