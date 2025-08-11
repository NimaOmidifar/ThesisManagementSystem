from src.main.LoginAndChangePass import LoginAndChangePass
from src.main.Student import Student

# m = LoginAndChangePass("9")
# print(m.login("8821"))
#
# m.change_password("8821")
# print(m.login("8821"))
#
# s = LoginAndChangePass("5", "master")
# print(s.login("7513"))
#
# s.change_password("1111")
# print(s.login("7513"))

s = Student("9", "8821")
s.courses_print()