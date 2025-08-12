from datetime import datetime

from src.main.FileManager import FileManager
from src.main.LoginAndChangePass import LoginAndChangePass

class Student:
    def __init__(self, student_id, password):
        self.student_id = student_id
        self.password = password

    def take_thesis(self, thesis_id):
        course_obj = FileManager("../resources/data/Courses.json")
        course_list = course_obj.file_reader()

        for course in course_list:
            if course["id"] == thesis_id:
                capacity = int(course["capacity"])
                if capacity != 0:
                    capacity -= 1
                    course["capacity"] = capacity
                    course_obj.file_writer(course_list)

                    student_file = FileManager("../resources/data/Students.json")
                    student_list = student_file.file_reader()
                    request_date = None
                    for student in student_list:
                        if student["id"] == self.student_id:
                            request_date = datetime.now().strftime("%d/%m/%Y")
                            student["request"]["status"] = "pending"
                            student["request"]["date"] = request_date
                            student_file.file_writer(student_list)
                            break

                    master_file = FileManager("../resources/data/Masters.json")
                    master_list = master_file.file_reader()
                    for master in master_list:
                        if course["master"] == master["name"]:
                            master["capacity"]["advisor"] -=  1
                            master["requests"].append({"requester_id" : self.student_id, "date" : request_date})
                            master_file.file_writer(master_list)
                            break

                    print("The unit was successfully reserved.")
                    break
                else:
                    print("The course is full.")

                break

    def status_print(self):
        student_file = FileManager("../resources/data/Students.json")
        student_list = student_file.file_reader()
        for student in student_list:
            if student["id"] == self.student_id:
                print(f"date: {student['request']['date']}\nstatus: {student['request']['status']}")
                break

    def courses_print(self):
        course_obj = FileManager("../resources/data/Courses.json")
        course_list = course_obj.file_reader()

        for course in course_list:
            print(f"id: {course['id']}\ntitle: {course['title']}\nmaster: {course['master']}\nyear: {course['year']}\nsemester: {course['semester']}\ncapacity: {course['capacity']}")
            for _ in course['resources']:
                print(_, end = ", ")
            print(f"\nsessions: {course['sessions']}\nunits: {course['units']}")
            print("-----------------------------------")