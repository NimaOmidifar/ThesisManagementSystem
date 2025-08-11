from src.main.LoginAndChangePass import LoginAndChangePass

m = LoginAndChangePass("9")
print(m.master_login("8821"))

m.master_change_password("8821")
print(m.master_login("8821"))

s = LoginAndChangePass("5")
print(s.student_login("7513"))

s.student_change_password("1111")
print(s.student_login("7513"))