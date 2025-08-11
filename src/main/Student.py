from src.main.FileManager import FileManager
from src.main.LoginAndChangePass import LoginAndChangePass

class Student:
    def __init__(self, student_id, password):
        self.student_id = student_id
        self.password = password

    def courses_print(self):
        course_obj = FileManager("../resources/data/Courses.json")
        course_list = course_obj.file_reader()

        for course in course_list:
            print(f"id: {course['id']}\ntitle: {course['title']}\nmaster: {course['master']}\nyear: {course['year']}\nsemester: {course['semester']}\ncapacity: {course['capacity']}")
            for _ in course['resources']:
                print(_, end = ", ")
            print(f"\nsessions: {course['sessions']}\nunits: {course['units']}")
            print("-----------------------------------")