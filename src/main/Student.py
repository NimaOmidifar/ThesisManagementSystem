from datetime import datetime
from FileManager import *
from LoginAndChangePass import *

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
                                return "You reserved an unit before."

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
                                    master["thesis_requests"].append({"requester_id": self.student_id, "date": request_date})
                                    master_file.file_writer(master_list)
                                    break

                            return "The course was successfully reserved."
                return "The course is full."
        return "There is no course with that ID."

    def take_thesis_defense(self, title, abstract, keywords, pdf_path, first_page_path, last_page_path):
        student_obj = FileManager("../resources/data/Students.json")
        student_list = student_obj.file_reader()
        for student in student_list:
            if student["id"] == self.student_id:
                if student["defense_request"]["status"] in ["no_request", "rejected"]:
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

                            pdf_name = f"thesis_{defense_id}.pdf"
                            first_page_extension = first_page_path[first_page_path.rfind(".") + 1:]
                            first_page_name = f"first_page_{defense_id}.{first_page_extension}"
                            last_pege_extension = last_page_path[last_page_path.rfind(".") + 1:]
                            last_page_name = f"last_page_{defense_id}.{last_pege_extension}"

                            defense_dic = {
                                "id": defense_id,
                                "student_id": self.student_id,
                                "student_name": student["name"],
                                "title": title,
                                "abstract": abstract,
                                "keywords": keywords,
                                "pdf_name": pdf_name,
                                "first_page_name": first_page_name,
                                "last_page_name": last_page_name,
                                "date": date_now_str
                            }

                            student["defense_request"]["status"] = "pending"
                            student["defense_request"]["date"] = date_now_str
                            student["defense_request"]["defense_id"] = defense_id

                            master_obj = FileManager("../resources/data/Masters.json")
                            master_list = master_obj.file_reader()
                            for master in master_list:
                                if master["id"] == student["thesis_request"]["master_id"]:
                                    if master["capacity"]["advisor"] == 0:
                                        return "The capacity if advisor is full."
                                    master["capacity"]["advisor"] -= 1
                                    master["defense_requests"].append({"requester_id": self.student_id, "date": date_now_str, "defense_id": defense_id})

                                    defense_list.append(defense_dic)
                                    defense_obj.file_writer(defense_list)

                                    student_obj.save_thesis(pdf_path, pdf_name, first_page_path, first_page_name, last_page_path, last_page_name)

                                    student_obj.file_writer(student_list)

                                    master_obj.file_writer(master_list)
                                    break
                            return "The request was successfully send."
                        return "Three months must have passed since the unit registration."
                    return "Wait for master decision."
                return "You reserved a thesis defense before."

    def status_print(self, type = "thesis"):
        student_file = FileManager("../resources/data/Students.json")
        student_list = student_file.file_reader()
        if type == "thesis":
            for student in student_list:
                if student["id"] == self.student_id:
                    return student['thesis_request']['date'], student['thesis_request']['status']
        else:
            for student in student_list:
                if student["id"] == self.student_id:
                    return student['defense_request']['date'], student['defense_request']['status']


    def final_status_print(self):
        master_name = " "
        internal_examiner_grade = " "
        external_examiner_grade = " "
        final_grade = " "
        status = " "
        next_date = " "
        final_list = []

        student_file = FileManager("../resources/data/Students.json")
        student_list = student_file.file_reader()
        for student in student_list:
            if student["id"] == self.student_id:
                master_file = FileManager("../resources/data/Masters.json")
                master_list = master_file.file_reader()
                for master in master_list:
                    if master["id"] == student["thesis_request"]["master_id"]:
                        master_name = master["name"]
                        break

                internal_examiner_grade = student["defense_result"]["internal_examiner_grade"]
                external_examiner_grade = student["defense_result"]["external_examiner_grade"]
                final_grade = student["defense_result"]["final_grade"]
                status = student["defense_result"]["result"]
                next_date = student["defense_result"]["next_date"]
                final_list.append(master_name)
                final_list.append(internal_examiner_grade)
                final_list.append(external_examiner_grade)
                final_list.append(final_grade)
                final_list.append(status)
                final_list.append(next_date)
                break

        return final_list