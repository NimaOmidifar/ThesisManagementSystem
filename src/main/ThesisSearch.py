from datetime import datetime

from src.main.FileManager import FileManager


class ThesisSearch:
    def __init__(self, title, master_name, keyword, author, year, examiner):
        self.title = title
        self.master_name = master_name
        self.keyword = keyword
        self.author = author
        self.year = year
        self.examiner = examiner

    def search(self):
        final_list = []
        requested_dic = {}
        if self.title:
            requested_dic["title"] = self.title
        if self.master_name:
            requested_dic["master_name"] = self.master_name
        if self.keyword:
            requested_dic["keywords"] = self.keyword
        if self.author:
            requested_dic["author"] = self.author
        if self.year:
            requested_dic["date"] = self.year
        if self.examiner:
            requested_dic["examiners"] = self.examiner

        if not requested_dic:
            final_list = self.print_all()
            return final_list

        successful_defenses_obj = FileManager("../resources/data/Successful_defenses.json")
        successful_defenses_list = successful_defenses_obj.file_reader()
        successful_defenses_list_copy = successful_defenses_list.copy()
        for successful_defenses in successful_defenses_list:
            for key, value in successful_defenses.items():
                if key in requested_dic:
                    flag = False
                    if key == "date":
                        str_date = successful_defenses["date"]
                        date = datetime.strptime(str_date, "%d/%m/%Y")
                        if str(date.year) == self.year:
                            flag = True
                    elif key == "examiners":
                        if self.examiner in value:
                            flag = True
                    elif key == "keywords":
                        if self.keyword in value:
                            flag = True
                    elif  value == requested_dic[key]:
                        flag = True

                    if flag:
                        title = successful_defenses["title"]
                        abstract = successful_defenses["abstract"]
                        keywords = successful_defenses["keywords"]
                        author_id = successful_defenses["student_id"]
                        author = successful_defenses["student_name"]
                        date = successful_defenses["date"]
                        examiners = successful_defenses["examiners"]
                        master = successful_defenses["master"]
                        score = successful_defenses["score"]
                        sub_tuple = (title, abstract, keywords, author_id, author, date, examiners, master, score)
                        final_list.append(sub_tuple)

        return final_list

    def print_all(self):
        final_list = []

        successful_defenses_obj = FileManager("../resources/data/Successful_defenses.json")
        successful_defenses_list = successful_defenses_obj.file_reader()
        for successful_defenses in successful_defenses_list:
            title = successful_defenses["title"]
            abstract = successful_defenses["abstract"]
            keywords = successful_defenses["keywords"]
            author_id = successful_defenses["student_id"]
            author = successful_defenses["student_name"]
            date = successful_defenses["date"]
            examiners = successful_defenses["examiners"]
            master = successful_defenses["master"]
            score = successful_defenses["score"]
            sub_tuple = (title, abstract, keywords, author_id, author, date, examiners, master, score)
            final_list.append(sub_tuple)

        return final_list
