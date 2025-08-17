from datetime import datetime, timedelta
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
                        master["thesis_requests"].remove(master["thesis_requests"][index])

                        student_obj = FileManager("../resources/data/Students.json")
                        student_list = student_obj.file_reader()
                        for student in student_list:
                            if student["id"] == requester_id:
                                if decision:
                                    student["thesis_request"]["status"] = "accepted"
                                    student_obj.file_writer(student_list)
                                    master_obj.file_writer(master_list)
                                    return "The student was accepted."
                                else:
                                    student["thesis_request"]["status"] = "rejected"

                                    master["capacity"]["advisor"] = master["capacity"]["advisor"] + 1

                                    course_obj = FileManager("../resources/data/Courses.json")
                                    course_list = course_obj.file_reader()
                                    for course in course_list:
                                        if course["id"] == student["thesis_request"]["course_id"]:
                                            course["capacity"] = course["capacity"] + 1
                                            course_obj.file_writer(course_list)
                                            student_obj.file_writer(student_list)
                                            master_obj.file_writer(master_list)
                                            return "The student was rejected."
                return "There is no student with that ID."



    def thesis_defense_decision(self, requester_id, decision = True, internal_examiner_id = -1, external_examiner_name = "", date = ""):
        try:
            requester_id = int(requester_id)
        except:
            return "Invalid student id."
        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        for master in master_list:
            if master["id"] == self.master_id:
                request_list = master["defense_requests"]

                for index, request in enumerate(request_list):
                    if request["requester_id"] == requester_id:
                        student_obj = FileManager("../resources/data/Students.json")
                        student_list = student_obj.file_reader()
                        for student in student_list:
                            if student["id"] == requester_id:
                                if decision:
                                    try:
                                        internal_examiner_id = int(internal_examiner_id)
                                    except:
                                        return "Invalid internal examiner id."
                                    if external_examiner_name == "":
                                        return "External examiner name must not be empty."
                                    defense_obj = FileManager("../resources/data/Defenses.json")
                                    defense_list = defense_obj.file_reader()
                                    defense_list_copy = defense_list.copy()

                                    defense_id = ""
                                    for defense in defense_list_copy:
                                        if defense["student_id"] == requester_id:
                                            defense_id = defense["id"]
                                            break

                                    message = self.choose_examiner(requester_id, student["name"], defense_id, internal_examiner_id, external_examiner_name, date)
                                    if message == "The defense was successfully reserved.":
                                        student["defense_request"]["status"] = "accepted"
                                        student_obj.file_writer(student_list)
                                    return message

                                else:
                                    student["defense_request"]["status"] = "rejected"

                                    master["capacity"]["advisor"] = master["capacity"]["advisor"] + 1

                                    defense_obj = FileManager("../resources/data/Defenses.json")
                                    defense_list = defense_obj.file_reader()
                                    defense_list_copy = defense_list.copy()

                                    for defense_index, defense in enumerate(defense_list_copy):
                                        if defense["id"] == master["defense_requests"][index]["defense_id"]:
                                            FileManager(defense["pdf_name"]).delete_file()
                                            FileManager(defense["first_page_name"]).delete_file()
                                            FileManager(defense["last_page_name"]).delete_file()

                                            defense_list.remove(defense_list[defense_index])
                                            break


                                    master["defense_requests"].remove(master["defense_requests"][index])
                                    master_obj.file_writer(master_list)

                                    defense_obj.file_writer(defense_list)
                                    student_obj.file_writer(student_list)
                                    return "The defense was successfully rejected."
                return "There is no student with that ID."

    def choose_examiner(self, requester_id, requester_name, defense_id, internal_examiner_id, external_examiner_name, date):
        try:
            defense_date = datetime.strptime(date, "%d/%m/%Y").date()
        except:
            return "Invalid date."
        now = datetime.now().date()

        if defense_date > now:
            master_obj = FileManager("../resources/data/Masters.json")
            master_list = master_obj.file_reader()
            for master in master_list:
                if master["id"] == internal_examiner_id:
                    if master["capacity"]["examiner"] != 0:
                        master["capacity"]["examiner"] = master["capacity"]["examiner"] - 1

                        for advisor in master_list:
                            if advisor["id"] == self.master_id:
                                for index, request in enumerate(advisor["defense_requests"]):
                                    if request["requester_id"] == requester_id:
                                        advisor["defense_requests"].remove(advisor["defense_requests"][index])
                                        break

                                dic = {
                                    "requester_id": requester_id,
                                    "requester_name": requester_name,
                                    "internal_examiner_name": advisor["name"],
                                    "external_examiner_name": external_examiner_name,
                                    "date": date,
                                    "defense_id": defense_id
                                }

                                advisor["defenses"].append(dic)
                                master["examiner_defense"].append(dic)

                                master_obj.file_writer(master_list)

                        return "The defense was successfully reserved."
                    return "The internal master is busy."
            return "There is no such internal master."
        return "It's past time."

    def register_thesis_defense_grade_internal(self, requester_id, grade):
        try:
            requester_id = int(requester_id)
        except:
            return "Invalid ID."
        try:
            grade = float(grade)
        except:
            return "Invalid grade."
        if not 0 <= grade <= 20:
            return "Invalid grade."

        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        for master in master_list:
            if master["id"] == self.master_id:
                for index, request in enumerate(master["examiner_defense"]):
                    if request["requester_id"] == requester_id:
                        defense_date = datetime.strptime(request["date"], "%d/%m/%Y").date()
                        now = datetime.now().date()
                        if defense_date > now:
                            return "The defense has not yet been made."

                        student_obj = FileManager("../resources/data/Students.json")
                        student_list = student_obj.file_reader()
                        for student in student_list:
                            if student["id"] == requester_id:
                                student["defense_result"]["internal_examiner_grade"] = grade
                                if student["defense_result"]["external_examiner_grade"] != "no_grade":
                                    average = round((student["defense_result"]["external_examiner_grade"] + grade) / 2,
                                                    2)
                                    student["defense_result"]["final_grade"] = average
                                    if average >= 12:
                                        student["defense_result"]["result"] = "accepted"

                                        master["examiner_defense"].remove(request)
                                        master_obj.file_writer(master_list)

                                        advisor_obj = FileManager("../resources/data/Masters.json")
                                        advisor_list = advisor_obj.file_reader()
                                        for advisor in advisor_list:
                                            for index, defense_req in enumerate(advisor["defenses"]):
                                                if defense_req["requester_id"] == requester_id:
                                                    advisor["defenses"].remove(defense_req)
                                                    break
                                        defense_obj = FileManager("../resources/data/Defenses.json")
                                        defense_list = defense_obj.file_reader()
                                        defense_list_copy = defense_list.copy()
                                        dic = {}
                                        for defense in defense_list_copy:
                                            if defense["student_id"] == requester_id:
                                                dic = defense
                                                dic[
                                                    "examiners"] = f"{request["internal_examiner_name"]}, {request['external_examiner_name']}"
                                                score = ""
                                                if 17 <= average <= 20:
                                                    score = "A"
                                                elif 13 <= average < 17:
                                                    score = "B"
                                                elif 10 <= average < 13:
                                                    score = "C"
                                                dic["date"] = defense_date.strftime("%d/%m/%Y")
                                                dic["score"] = score
                                                defense_list.remove(defense)
                                                defense_obj.file_writer(defense_list)
                                                break
                                        successful_defense_obj = FileManager(
                                            "../resources/data/Successful_defenses.json")
                                        successful_list = successful_defense_obj.file_reader()
                                        successful_list.append(dic)
                                        successful_defense_obj.file_writer(successful_list)

                                        student_obj.file_writer(student_list)
                                        advisor_obj.file_writer(advisor_list)
                                        return "Grade successfully recorded."

                                    else:
                                        student["defense_result"]["result"] = "rejected"

                                        defense_date = defense_date + timedelta(days=30)
                                        request["date"] = defense_date.strftime("%d/%m/%Y")

                                        advisor_obj = FileManager("../resources/data/Masters.json")
                                        advisor_list = advisor_obj.file_reader()
                                        for advisor in advisor_list:
                                            if advisor["name"] == request["external_examiner_name"]:
                                                advisor["defenses"]["date"] = defense_date.strftime("%d/%m/%Y")
                                                break

                                        student["defense_result"]["next_date"] = defense_date.strftime("%d/%m/%Y")

                                        master_obj.file_writer(master_list)
                                        student_obj.file_writer(student_list)
                                        advisor_obj.file_writer(advisor_list)
                                        return "Grade successfully recorded."
                                else:
                                    student_obj.file_writer(student_list)
                                    return "Grade successfully recorded."
                return "There is no student with that ID."

    def register_thesis_defense_grade_external(self, requester_id, grade):
        try:
            requester_id = int(requester_id)
        except:
            return "Invalid ID."
        try:
            grade = float(grade)
        except:
            return "Invalid grade."
        if not 0 <= grade <= 20:
            return "Invalid grade."

        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        for master in master_list:
            if master["id"] == self.master_id:
                for index, request in enumerate(master["defenses"]):
                    if request["requester_id"] == requester_id:
                        defense_date = datetime.strptime(request["date"], "%d/%m/%Y").date()
                        now = datetime.now().date()
                        if defense_date > now:
                            return "The defense has not yet been made."

                        student_obj = FileManager("../resources/data/Students.json")
                        student_list = student_obj.file_reader()
                        for student in student_list:
                            if student["id"] == requester_id:
                                student["defense_result"]["external_examiner_grade"] = grade
                                if student["defense_result"]["internal_examiner_grade"] != "no_grade":
                                    average = round((student["defense_result"]["internal_examiner_grade"] + grade) / 2,
                                                    2)
                                    student["defense_result"]["final_grade"] = average
                                    if average >= 12:
                                        student["defense_result"]["result"] = "accepted"

                                        master["defenses"].remove(request)
                                        master_obj.file_writer(master_list)

                                        advisor_obj = FileManager("../resources/data/Masters.json")
                                        advisor_list = advisor_obj.file_reader()
                                        for advisor in advisor_list:
                                            for index, defense_req in enumerate(advisor["examiner_defense"]):
                                                if defense_req["requester_id"] == requester_id:
                                                    advisor["examiner_defense"].remove(defense_req)
                                                    break
                                        defense_obj = FileManager("../resources/data/Defenses.json")
                                        defense_list = defense_obj.file_reader()
                                        defense_list_copy = defense_list.copy()
                                        dic = {}
                                        for defense in defense_list_copy:
                                            if defense["student_id"] == requester_id:
                                                dic = defense
                                                dic[
                                                    "examiners"] = f"{request["internal_examiner_name"]}, {request['external_examiner_name']}"
                                                score = ""
                                                if 17 <= average <= 20:
                                                    score = "A"
                                                elif 13 <= average < 17:
                                                    score = "B"
                                                elif 10 <= average < 13:
                                                    score = "C"
                                                dic["date"] = defense_date.strftime("%d/%m/%Y")
                                                dic["score"] = score
                                                defense_list.remove(defense)
                                                defense_obj.file_writer(defense_list)
                                                break
                                        successful_defense_obj = FileManager(
                                            "../resources/data/Successful_defenses.json")
                                        successful_list = successful_defense_obj.file_reader()
                                        successful_list.append(dic)
                                        successful_defense_obj.file_writer(successful_list)

                                        student_obj.file_writer(student_list)
                                        advisor_obj.file_writer(advisor_list)
                                        return "Grade successfully recorded."

                                    else:
                                        student["defense_result"]["result"] = "rejected"

                                        defense_date = defense_date + timedelta(days=30)
                                        request["date"] = defense_date.strftime("%d/%m/%Y")

                                        advisor_obj = FileManager("../resources/data/Masters.json")
                                        advisor_list = advisor_obj.file_reader()
                                        for advisor in advisor_list:
                                            if advisor["name"] == request["internal_examiner_name"]:
                                                advisor["examiner_defense"]["date"] = defense_date.strftime("%d/%m/%Y")
                                                break

                                        student["defense_result"]["next_date"] = defense_date.strftime("%d/%m/%Y")

                                        master_obj.file_writer(master_list)
                                        student_obj.file_writer(student_list)
                                        advisor_obj.file_writer(advisor_list)
                                        return "Grade successfully recorded."
                                else:
                                    student_obj.file_writer(student_list)
                                    return "Grade successfully recorded."
                return "There is no student with that ID."


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
                        break
            return final_list

    def internal_examiner_defenses_print(self):
        final_list = []

        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        for master in master_list:
            if master["id"] == self.master_id:
                if not master["examiner_defense"]:
                    return final_list

                for defense in master["examiner_defense"]:
                    defense_id = defense["defense_id"]
                    student_id = defense["requester_id"]
                    student_name = defense["requester_name"]
                    examiners_name = f"{defense["internal_examiner_name"]}, {defense['external_examiner_name']}"
                    defense_date = defense["date"]
                    sub_tuple = (defense_id, student_id, student_name, examiners_name, defense_date)
                    final_list.append(sub_tuple)
                break
        return final_list

    def external_examiner_defenses_print(self):
        final_list = []

        master_obj = FileManager("../resources/data/Masters.json")
        master_list = master_obj.file_reader()
        for master in master_list:
            if master["id"] == self.master_id:
                if not master["defenses"]:
                    return final_list

                for defense in master["defenses"]:
                    defense_id = defense["defense_id"]
                    student_id = defense["requester_id"]
                    student_name = defense["requester_name"]
                    examiners_name = f"{defense["internal_examiner_name"]}, {defense['external_examiner_name']}"
                    defense_date = defense["date"]
                    sub_tuple = (defense_id, student_id, student_name, examiners_name, defense_date)
                    final_list.append(sub_tuple)
                break
        return final_list