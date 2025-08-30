import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from FileManager import *
from LoginAndChangePass import *
from Master import *
from Student import *
from ThesisSearch import *


class GUI():
    def __init__(self):
        self.login_page()

    def login_page(self):
        WIDTH = 950
        HEIGHT = 650
        FORM_COLOR = "#000033"
        BTN_COLOR = "#2E8BC0"
        INPUT_COLOR = "#0C2D48"

        root = tk.Tk()
        root.title('Login Page')

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2
        root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        root.resizable(False, False)

        try:
            image = Image.open("../resources/picture/background.png")
            image = image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            bg_label = tk.Label(root, image=photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.image = photo
        except Exception as e:
            print(f"Error: {e}")


        # -------------login form---------------
        LOGIN_FRAME_WIDTH = 400
        LOGIN_FRAME_HEIGHT = 470
        ENTRY_WIDTH = 300
        ENTRY_HEIGHT = 40

        login_frame = tk.Frame(root, bg = FORM_COLOR)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=LOGIN_FRAME_WIDTH, height=LOGIN_FRAME_HEIGHT)

        login_label = tk.Label(login_frame, text="Login Page", font=("Arial", 20), bg=FORM_COLOR, fg="white")
        login_label.place(x=130, y=20)

        id_label = tk.Label(login_frame, text="ID:", font=("Arial", 11), bg=FORM_COLOR, fg="white")
        id_label.place(x=50, y=90)
        id_entry = tk.Entry(login_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
        id_entry.place(x=50, y=120, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

        password_label = tk.Label(login_frame, text="password:", font=("Arial", 11), bg=FORM_COLOR, fg="white")
        password_label.place(x=50, y=180)
        password_entry = tk.Entry(login_frame, bg=INPUT_COLOR,  insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0, show="•")
        password_entry.place(x=50, y=210,  width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

        def forgot_pass_action(event):
            login_frame.place_forget()
            # -------------------------forgot password frame-----------------------------
            forgot_frame = tk.Frame(root, bg=FORM_COLOR)
            forgot_frame.place(relx=0.5, rely=0.5, anchor="center", width=LOGIN_FRAME_WIDTH, height=LOGIN_FRAME_HEIGHT)

            def turn_back_action():
                login_frame.place(relx=0.5, rely=0.5, anchor="center", width=LOGIN_FRAME_WIDTH, height=LOGIN_FRAME_HEIGHT)
                forgot_frame.place_forget()

            back_btn = tk.Button(forgot_frame, text="⬅ back", font=("Arial", 8), bg=BTN_COLOR,fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6",cursor="hand2", command=turn_back_action)
            back_btn.place(x=0, y=0, width=50, height=50)

            forgot_label = tk.Label(forgot_frame, text="Reset your password", font=("Arial", 20), bg=FORM_COLOR, fg="white")
            forgot_label.place(x=70, y=20)

            id_forgot_label = tk.Label(forgot_frame, text="ID:", font=("Arial", 11), bg=FORM_COLOR, fg="white")
            id_forgot_label.place(x=50, y=90)
            id_forgot_entry = tk.Entry(forgot_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white",bd=0, highlightthickness=0)
            id_forgot_entry.place(x=50, y=120, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            password_forgot_label = tk.Label(forgot_frame, text="new password:", font=("Arial", 11), bg=FORM_COLOR, fg="white")
            password_forgot_label.place(x=50, y=180)
            password_forgot_entry = tk.Entry(forgot_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11),fg="white", bd=0, highlightthickness=0, show="•")
            password_forgot_entry.place(x=50, y=210, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            def change_password_action():
                id = id_forgot_entry.get().strip()
                password = password_forgot_entry.get().strip()

                login = LoginAndChangePass(id)
                first_bool = login.change_password(password)
                second_bool = login.change_password(password, "master")
                if first_bool or second_bool:
                    warn_label = tk.Label(forgot_frame, text="Password changed successfully.", font=("Arial", 11), bg=FORM_COLOR, fg="green")
                    warn_label.place(x=90, y=310)
                else:
                    warn_label = tk.Label(forgot_frame, text="There is no such user!", font=("Arial", 11), bg=FORM_COLOR, fg="red")
                    warn_label.place(x=125, y=310)

            change_pass_btn = tk.Button(forgot_frame, text="Change password", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0,highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command= change_password_action)
            change_pass_btn.place(x=50, y=360, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

        def on_enter(event):
            forgot_pass_label.config(fg="#ADD8E6")

        def on_leave(event):
            forgot_pass_label.config(fg="white")

        forgot_pass_label = tk.Label(login_frame, text="Forgot password?", font=("Arial", 11), bg=FORM_COLOR, fg="white", cursor="hand2")
        forgot_pass_label.place(x=45, y=260)
        forgot_pass_label.bind("<Button-1>", forgot_pass_action)
        forgot_pass_label.bind("<Enter>", on_enter)
        forgot_pass_label.bind("<Leave>", on_leave)

        def login_action():
            id = id_entry.get().strip()
            password = password_entry.get().strip()

            login = LoginAndChangePass(id)
            if login.login(password):
                name = login.get_name()
                student = Student(id, password)
                self.student_page(name, student)
                root.destroy()

            elif login.login(password, "master"):
                name = login.get_name()
                master = Master(id, password)
                self.master_page(name, master)
                root.destroy()
            else:
                warn_label = tk.Label(login_frame, text="There is no such user!", font=("Arial", 11), bg=FORM_COLOR,fg="red")
                warn_label.place(x=125, y=310)


        login_btn = tk.Button(login_frame, text="Login", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=login_action)
        login_btn.place(x=50, y=360, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

        root.mainloop()

    def student_page(self, name, student_object):
        WIDTH = 950
        HEIGHT = 650
        ENTRY_WIDTH = 300
        ENTRY_HEIGHT = 40
        LEFT_COLOR = "#0C2D48"
        RIGHT_COLOR = "#081D2B"
        LINE_COLOR = "#99FFFF"
        BTN_COLOR = "#2E8BC0"
        INPUT_COLOR = "#0C2D48"

        student_form = tk.Tk()
        student_form.title('Student Page')

        screen_width = student_form.winfo_screenwidth()
        screen_height = student_form.winfo_screenheight()
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2
        student_form.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        student_form.resizable(False, False)

        #-----------------------left frame--------------------------------
        left_frame = tk.Frame(student_form, bg=LEFT_COLOR)
        left_frame.place(x=0, y=0, width=230, height=HEIGHT)

        right_line = tk.Canvas(left_frame, width=2, height=HEIGHT, bg=LINE_COLOR, highlightthickness=0)
        right_line.place(x=228, y=0)

        name_label = tk.Label(left_frame, text=name, font=("Arial", 11), bg=LEFT_COLOR, fg="white")
        name_label.place(x=60, y=130)

        student_label = tk.Label(left_frame, text="Student", font=("Arial", 8), bg=LEFT_COLOR, fg="white")
        student_label.place(x=85, y=155)

        def courses_btn_action():
            take_thesis_frame.place_forget()
            take_thesis_defense_frame.place_forget()
            theses_bank_frame.place_forget()
            thesis_defense_result_frame.place_forget()
            course_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            courses_btn.config(bg=RIGHT_COLOR)
            take_thesis_btn.config(bg=BTN_COLOR)
            take_thesis_defense_btn.config(bg=BTN_COLOR)
            thesis_defense_result_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)


            canvas = tk.Canvas(course_frame, bg=RIGHT_COLOR, highlightthickness=0)
            scrollbar = tk.Scrollbar(course_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=RIGHT_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            course_obj = FileManager("../resources/data/Courses.json")
            course_list = course_obj.file_reader()
            for course in course_list:
                resources = ", ".join(course['resources'])
                tk.Label(scrollable_frame, width=93, text=f"id: {course['id']}\ntitle: {course['title']}\nmaster: {course['master']}\nyear: {course['year']}\nsemester: {course['semester']}\ncapacity: {course['capacity']}\nresources: {resources}\nsessions: {course['sessions']}\nunits: {course['units']}",font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left", padx=10).pack(padx= 15, pady=7)


        courses_btn = tk.Button(left_frame, text="Courses", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=courses_btn_action)
        courses_btn.place(x=0, y=260, width=228, height=60)

        line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        line_between.place(x=0, y=320)

        def take_thesis_action():
            for widget in course_frame.winfo_children():
                widget.destroy()
            take_thesis_defense_frame.place_forget()
            theses_bank_frame.place_forget()
            thesis_defense_result_frame.place_forget()
            take_thesis_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            take_thesis_btn.config(bg=RIGHT_COLOR)
            courses_btn.config(bg=BTN_COLOR)
            take_thesis_defense_btn.config(bg=BTN_COLOR)
            thesis_defense_result_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)

            thesis_id_label = tk.Label(take_thesis_frame, text="Thesis id:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            thesis_id_label.place(x=65, y=114)
            thesis_id_entry = tk.Entry(take_thesis_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            thesis_id_entry.place(x=135, y=105, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            left_line = tk.Canvas(take_thesis_frame, width=60, height=2, bg=LINE_COLOR, highlightthickness=0)
            left_line.place(x=15, y=205)

            thesis_id_label = tk.Label(take_thesis_frame, text="Request history", font=("Arial", 14), bg=RIGHT_COLOR, fg="white")
            thesis_id_label.place(x=65, y=190)

            right_line = tk.Canvas(take_thesis_frame, width=495, height=2, bg=LINE_COLOR, highlightthickness=0)
            right_line.place(x=205, y=205)

            status_tuple = student_object.status_print()
            date_label = tk.Label(take_thesis_frame, text=f"Request date: {status_tuple[0]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            date_label.place(x=65, y=250)
            status_label = tk.Label(take_thesis_frame, text=f"Status: {status_tuple[1]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            status_label.place(x=65, y=280)

            def send_request_action():
                input_id = thesis_id_entry.get().strip()
                message = student_object.take_thesis(input_id)

                message_label = tk.Label(take_thesis_frame, text=message, font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                message_label.place(x=220, y=430)

            send_request_btn = tk.Button(take_thesis_frame, text="Send request", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=send_request_action)
            send_request_btn.place(x=65, y=500, width=228, height=60)

        take_thesis_btn = tk.Button(left_frame, text="Take thesis", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=take_thesis_action)
        take_thesis_btn.place(x=0, y=322, width=228, height=60)

        second_line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        second_line_between.place(x=0, y=382)

        def take_thesis_defense_action():
            for widget in course_frame.winfo_children():
                widget.destroy()
            take_thesis_frame.place_forget()
            theses_bank_frame.place_forget()
            thesis_defense_result_frame.place_forget()
            take_thesis_defense_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            take_thesis_defense_btn.config(bg=RIGHT_COLOR)
            courses_btn.config(bg=BTN_COLOR)
            take_thesis_btn.config(bg=BTN_COLOR)
            thesis_defense_result_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)

            title_label = tk.Label(take_thesis_defense_frame, text="Title:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            title_label.place(x=65, y=44)
            title_entry = tk.Entry(take_thesis_defense_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            title_entry.place(x=135, y=35, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            abstract_label = tk.Label(take_thesis_defense_frame, text="Abstract:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            abstract_label.place(x=65, y=99)
            abstract_entry = tk.Text(take_thesis_defense_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            abstract_entry.place(x=135, y=90, width=ENTRY_WIDTH, height=ENTRY_HEIGHT * 3)

            keyword_label = tk.Label(take_thesis_defense_frame, text="keywords:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            keyword_label.place(x=65, y=234)
            keyword_entry = tk.Entry(take_thesis_defense_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            keyword_entry.place(x=135, y=225, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            pdf_path_label = tk.Label(take_thesis_defense_frame, text="pdf path:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            pdf_path_label.place(x=65, y=289)
            pdf_path_entry = tk.Entry(take_thesis_defense_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            pdf_path_entry.place(x=135, y=280, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            def pdf_path_browse_action():
                pdf_path = filedialog.askopenfilename(
                    title="Select a file",
                    filetypes=[("PDF files", "*.pdf")]
                )

                if pdf_path:
                    pdf_path_entry.delete(0, tk.END)
                    pdf_path_entry.insert(0, pdf_path)

            pdf_path_browse_btn = tk.Button(take_thesis_defense_frame, text="Browse", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=pdf_path_browse_action)
            pdf_path_browse_btn.place(x=450, y=280, width=80, height=ENTRY_HEIGHT)

            first_page_path_label = tk.Label(take_thesis_defense_frame, text="First page path:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            first_page_path_label.place(x=65, y=344)
            first_page_path_entry = tk.Entry(take_thesis_defense_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            first_page_path_entry.place(x=135, y=335, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            def first_page_path_browse_action():
                first_page_path = filedialog.askopenfilename(
                    title="Select a file",
                    filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
                )

                if first_page_path:
                    first_page_path_entry.delete(0, tk.END)
                    first_page_path_entry.insert(0, first_page_path)

            first_page_path_browse_btn = tk.Button(take_thesis_defense_frame, text="Browse", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=first_page_path_browse_action)
            first_page_path_browse_btn.place(x=450, y=335, width=80, height=ENTRY_HEIGHT)

            last_page_path_label = tk.Label(take_thesis_defense_frame, text="Last page path:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            last_page_path_label.place(x=65, y=399)
            last_page_path_entry = tk.Entry(take_thesis_defense_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            last_page_path_entry.place(x=135, y=390, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            def last_page_path_browse_action():
                last_page_path = filedialog.askopenfilename(
                    title="Select a file",
                    filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
                )

                if last_page_path:
                    last_page_path_entry.delete(0, tk.END)
                    last_page_path_entry.insert(0, last_page_path)

            last_page_path_browse_btn = tk.Button(take_thesis_defense_frame, text="Browse", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=last_page_path_browse_action)
            last_page_path_browse_btn.place(x=450, y=390, width=80, height=ENTRY_HEIGHT)

            left_line = tk.Canvas(take_thesis_defense_frame, width=60, height=2, bg=LINE_COLOR, highlightthickness=0)
            left_line.place(x=15, y=460)

            thesis_id_label = tk.Label(take_thesis_defense_frame, text="Request history", font=("Arial", 14), bg=RIGHT_COLOR, fg="white")
            thesis_id_label.place(x=65, y=445)

            right_line = tk.Canvas(take_thesis_defense_frame, width=495, height=2, bg=LINE_COLOR, highlightthickness=0)
            right_line.place(x=205, y=460)

            status_tuple = student_object.status_print("thesis_defense")
            date_label = tk.Label(take_thesis_defense_frame, text=f"Request date: {status_tuple[0]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            date_label.place(x=65, y=480)
            status_label = tk.Label(take_thesis_defense_frame, text=f"Status: {status_tuple[1]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            status_label.place(x=65, y=505)

            def send_request_action():
                title = title_entry.get().strip()
                abstract = abstract_entry.get("1.0", tk.END).strip()
                keywords = keyword_entry.get().strip()
                pdf_path = pdf_path_entry.get().strip()
                first_page_path = first_page_path_entry.get().strip()
                last_page_path = last_page_path_entry.get().strip()

                message = student_object.take_thesis_defense(title, abstract, keywords, pdf_path, first_page_path, last_page_path)

                message_label = tk.Label(take_thesis_defense_frame, text=message, font=("Arial", 11), bg=RIGHT_COLOR,fg="white")
                message_label.place(x=65, y=570)

            send_request_btn = tk.Button(take_thesis_defense_frame, text="Send request", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=send_request_action)
            send_request_btn.place(x=450, y=550, width=228, height=60)



        take_thesis_defense_btn = tk.Button(left_frame, text="take thesis defense", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=take_thesis_defense_action)
        take_thesis_defense_btn.place(x=0, y=384, width=228, height=60)

        line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        line_between.place(x=0, y=444)

        def thesis_defense_result_btn_action():
            for widget in course_frame.winfo_children():
                widget.destroy()
            take_thesis_frame.place_forget()
            theses_bank_frame.place_forget()
            take_thesis_defense_frame.place_forget()
            thesis_defense_result_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            thesis_defense_result_btn.config(bg=RIGHT_COLOR)
            courses_btn.config(bg=BTN_COLOR)
            take_thesis_btn.config(bg=BTN_COLOR)
            take_thesis_defense_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)

            left_line = tk.Canvas(thesis_defense_result_frame, width=60, height=2, bg=LINE_COLOR, highlightthickness=0)
            left_line.place(x=15, y=40)

            thesis_id_label = tk.Label(thesis_defense_result_frame, text="Defense history", font=("Arial", 14),
                                       bg=RIGHT_COLOR, fg="white")
            thesis_id_label.place(x=65, y=25)

            right_line = tk.Canvas(thesis_defense_result_frame, width=495, height=2, bg=LINE_COLOR,
                                   highlightthickness=0)
            right_line.place(x=205, y=40)

            status_list = student_object.final_status_print()

            title_label = tk.Label(thesis_defense_result_frame, text=f"Master: {status_list[0]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            title_label.place(x=65, y=75)

            abstract_label = tk.Label(thesis_defense_result_frame, text=f"internal examiner grade: {status_list[1]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            abstract_label.place(x=65, y=110)

            keyword_label = tk.Label(thesis_defense_result_frame, text=f"external examiner grade: {status_list[2]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            keyword_label.place(x=65, y=145)

            pdf_path_label = tk.Label(thesis_defense_result_frame, text=f"Final grade: {status_list[3]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            pdf_path_label.place(x=65, y=180)

            first_page_path_label = tk.Label(thesis_defense_result_frame, text=f"Status: {status_list[4]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            first_page_path_label.place(x=65, y=215)

            last_page_path_label = tk.Label(thesis_defense_result_frame, text=f"Next date: {status_list[5]}", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            last_page_path_label.place(x=65, y=250)

        thesis_defense_result_btn = tk.Button(left_frame, text="Thesis defense result", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=thesis_defense_result_btn_action)
        thesis_defense_result_btn.place(x=0, y=446, width=228, height=60)

        line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        line_between.place(x=0, y=506)

        def theses_bank_btn_action():
            for widget in course_frame.winfo_children():
                widget.destroy()
            take_thesis_frame.place_forget()
            take_thesis_defense_frame.place_forget()
            thesis_defense_result_frame.place_forget()
            theses_bank_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            theses_bank_btn.config(bg=RIGHT_COLOR)
            courses_btn.config(bg=BTN_COLOR)
            take_thesis_btn.config(bg=BTN_COLOR)
            thesis_defense_result_btn.config(bg=BTN_COLOR)
            take_thesis_defense_btn.config(bg=BTN_COLOR)

            canvas = tk.Canvas(theses_bank_frame, bg=RIGHT_COLOR, highlightthickness=0, width=600,
                               height=300)
            scrollbar = tk.Scrollbar(theses_bank_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=RIGHT_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.place(x=20, y=20, width=620, height=350)
            scrollbar.place(x=670, y=20, width=15, height=350)

            defenses_list = ThesisSearch("", "", "", "", "", "").print_all()
            for defense in defenses_list:
                tk.Label(scrollable_frame, width=90,
                         text=f"Title: {defense[0]}\nAbstract: {defense[1]}\nKeywords: {defense[2]}\nAuthor id: {defense[3]}\nAuthor: {defense[4]}\ndate: {defense[5]}\nexaminers: {defense[6]}\nmaster: {defense[7]}\nscore: {defense[8]}",
                         font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx=15,
                                                                                                        pady=7)

            title_label = tk.Label(theses_bank_frame, text="Title:", font=("Arial", 11),
                                   bg=RIGHT_COLOR, fg="white")
            title_label.place(x=15, y=399)
            title_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR,
                                   insertbackground="white",
                                   font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            title_entry.place(x=55, y=390, width=140, height=ENTRY_HEIGHT)

            master_name_label = tk.Label(theses_bank_frame, text="Master name:", font=("Arial", 11),
                                         bg=RIGHT_COLOR, fg="white")
            master_name_label.place(x=220, y=399)
            master_name_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                         font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            master_name_entry.place(x=320, y=390, width=140, height=ENTRY_HEIGHT)

            keyword_label = tk.Label(theses_bank_frame, text="Keyword:", font=("Arial", 11),
                                     bg=RIGHT_COLOR, fg="white")
            keyword_label.place(x=485, y=399)
            keyword_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                     font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            keyword_entry.place(x=555, y=390, width=140, height=ENTRY_HEIGHT)

            author_label = tk.Label(theses_bank_frame, text="Author:", font=("Arial", 11),
                                    bg=RIGHT_COLOR, fg="white")
            author_label.place(x=15, y=467)
            author_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                    font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            author_entry.place(x=70, y=460, width=140, height=ENTRY_HEIGHT)

            year_label = tk.Label(theses_bank_frame, text="Year:", font=("Arial", 11),
                                  bg=RIGHT_COLOR, fg="white")
            year_label.place(x=230, y=467)
            year_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                  font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            year_entry.place(x=275, y=460, width=140, height=ENTRY_HEIGHT)

            examiner_label = tk.Label(theses_bank_frame, text="Examiner:", font=("Arial", 11),
                                      bg=RIGHT_COLOR, fg="white")
            examiner_label.place(x=440, y=467)
            examiner_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                      font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            examiner_entry.place(x=520, y=460, width=140, height=ENTRY_HEIGHT)

            author_id_label = tk.Label(theses_bank_frame, text="Author id:", font=("Arial", 11),
                                       bg=RIGHT_COLOR, fg="white")
            author_id_label.place(x=15, y=567)
            author_id_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                       font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            author_id_entry.place(x=85, y=560, width=100, height=ENTRY_HEIGHT)

            def open_pdf_btn_action():
                if author_id_entry.get() == "":
                    warn_label = tk.Label(theses_bank_frame, text="author id must not empty.",
                                          font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                    warn_label.place(x=15, y=610)
                else:
                    author_id = int(author_id_entry.get().strip())
                    flag = False
                    for defense in defenses_list:
                        if defense[3] == author_id:
                            flag = True
                            file = FileManager(defense[9])
                            file.open_file()
                            break
                    if not flag:
                        warn_label = tk.Label(theses_bank_frame, text="There is no author with this id.",
                                              font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                        warn_label.place(x=15, y=610)

            open_pdf_btn = tk.Button(theses_bank_frame, text="Open pdf", font=("Arial", 11),
                                     bg=BTN_COLOR,
                                     fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2",
                                     command=open_pdf_btn_action)
            open_pdf_btn.place(x=200, y=560, width=100, height=ENTRY_HEIGHT)

            def search_btn_action():
                for widget in scrollable_frame.winfo_children():
                    widget.destroy()
                title = title_entry.get().strip()
                master_name = master_name_entry.get().strip()
                keyword = keyword_entry.get().strip()
                author = author_entry.get().strip()
                year = year_entry.get().strip()
                examiner = examiner_entry.get().strip()

                defenses_list = ThesisSearch(title, master_name, keyword, author, year, examiner).search()
                for defense in defenses_list:
                    tk.Label(scrollable_frame, width=90,
                             text=f"Title: {defense[0]}\nAbstract: {defense[1]}\nKeywords: {defense[2]}\nAuthor id: {defense[3]}\nAuthor: {defense[4]}\ndate: {defense[5]}\nexaminers: {defense[6]}\nmaster: {defense[7]}\nscore: {defense[8]}",
                             font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx=15,
                                                                                                            pady=7)

            search_btn = tk.Button(theses_bank_frame, text="Search", font=("Arial", 11),
                                   bg=BTN_COLOR,
                                   fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2",
                                   command=search_btn_action)
            search_btn.place(x=420, y=550, width=228, height=60)

        theses_bank_btn = tk.Button(left_frame, text="Theses Bank", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0,
                                    highlightthickness=0, activebackground="#ADD8E6", cursor="hand2",
                                    command=theses_bank_btn_action)
        theses_bank_btn.place(x=0, y=508, width=228, height=60)

        # -----------------------right frames--------------------------------
        right_frame = tk.Frame(student_form, bg=RIGHT_COLOR)
        right_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)

        course_frame = tk.Frame(student_form, bg=RIGHT_COLOR)

        take_thesis_frame = tk.Frame(student_form, bg=RIGHT_COLOR)
        take_thesis_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)

        take_thesis_defense_frame = tk.Frame(student_form, bg=RIGHT_COLOR)
        take_thesis_defense_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)

        thesis_defense_result_frame = tk.Frame(student_form, bg=RIGHT_COLOR)
        thesis_defense_result_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)

        theses_bank_frame = tk.Frame(student_form, bg=RIGHT_COLOR)


    def master_page(self, name, master_object):
        WIDTH = 950
        HEIGHT = 650
        ENTRY_WIDTH = 300
        ENTRY_HEIGHT = 40
        LEFT_COLOR = "#0C2D48"
        RIGHT_COLOR = "#081D2B"
        LINE_COLOR = "#99FFFF"
        BTN_COLOR = "#2E8BC0"
        INPUT_COLOR = "#0C2D48"

        master_form = tk.Tk()
        master_form.title('Master Page')

        screen_width = master_form.winfo_screenwidth()
        screen_height = master_form.winfo_screenheight()
        x = (screen_width - WIDTH) // 2
        y = (screen_height - HEIGHT) // 2
        master_form.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
        master_form.resizable(False, False)

        # -----------------------left frame--------------------------------
        left_frame = tk.Frame(master_form, bg=LEFT_COLOR)
        left_frame.place(x=0, y=0, width=230, height=HEIGHT)

        right_line = tk.Canvas(left_frame, width=2, height=HEIGHT, bg=LINE_COLOR, highlightthickness=0)
        right_line.place(x=228, y=0)

        name_label = tk.Label(left_frame, text=name, font=("Arial", 11), bg=LEFT_COLOR, fg="white")
        name_label.place(x=60, y=130)

        master_label = tk.Label(left_frame, text="Master", font=("Arial", 8), bg=LEFT_COLOR, fg="white")
        master_label.place(x=85, y=155)

        def thesis_request_btn_action():
            register_thesis_defense_grade_frame.place_forget()
            thesis_defense_request_frame.place_forget()
            register_external_examiner_grade_frame.place_forget()
            theses_bank_frame.place_forget()
            thesis_request_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            thesis_request_btn.config(bg=RIGHT_COLOR)
            thesis_defense_request_btn.config(bg=BTN_COLOR)
            register_thesis_defense_grade_btn.config(bg=BTN_COLOR)
            register_external_examiner_grade_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)

            canvas = tk.Canvas(thesis_request_frame, bg=RIGHT_COLOR, highlightthickness=0, width=600, height=300)
            scrollbar = tk.Scrollbar(thesis_request_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=RIGHT_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.place(x=20, y=20, width=620, height=350)
            scrollbar.place(x=670, y=20, width=15, height=350)

            request_list = master_object.thesis_requests_print()
            for request in request_list:
                tk.Label(scrollable_frame, width=90, text=f"Student id: {request[3]}\nStudent name: {request[2]}\nCourse name: {request[1]}\nDate: {request[0]}", font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx= 15, pady=7)

            student_id_label = tk.Label(thesis_request_frame, text="Student id:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            student_id_label.place(x=65, y=399)
            student_id_entry = tk.Entry(thesis_request_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            student_id_entry.place(x=140, y=390, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            combo = ttk.Combobox(thesis_request_frame, values=["accept", "reject"], state="readonly", style="Custom.TCombobox")
            combo.current(0)
            combo.place(x=460, y=390, width=70, height=40)

            def submit_btn_action():
                student_id = student_id_entry.get()

                decision = True
                if combo.get() == "reject":
                    decision = False
                message = master_object.thesis_decision(student_id, decision)

                message_label = tk.Label(thesis_request_frame, text=message, font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                message_label.place(x=65, y=520)

            submit_btn = tk.Button(thesis_request_frame, text="Submit", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=submit_btn_action)
            submit_btn.place(x=420, y=500, width=228, height=60)

        thesis_request_btn = tk.Button(left_frame, text="Thesis requests", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0,
                                highlightthickness=0, activebackground="#ADD8E6", cursor="hand2",
                                command=thesis_request_btn_action)
        thesis_request_btn.place(x=0, y=260, width=228, height=60)

        line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        line_between.place(x=0, y=320)

        def thesis_defense_request_btn_action():
            thesis_request_frame.place_forget()
            register_thesis_defense_grade_frame.place_forget()
            register_external_examiner_grade_frame.place_forget()
            theses_bank_frame.place_forget()
            thesis_defense_request_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            thesis_defense_request_btn.config(bg=RIGHT_COLOR)
            thesis_request_btn.config(bg=BTN_COLOR)
            register_thesis_defense_grade_btn.config(bg=BTN_COLOR)
            register_external_examiner_grade_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)

            canvas = tk.Canvas(thesis_defense_request_frame, bg=RIGHT_COLOR, highlightthickness=0, width=600, height=300)
            scrollbar = tk.Scrollbar(thesis_defense_request_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=RIGHT_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.place(x=20, y=20, width=620, height=270)
            scrollbar.place(x=670, y=20, width=15, height=270)

            request_list = master_object.thesis_defense_requests_print()
            for request in request_list:
                tk.Label(scrollable_frame, width=90, text=f"Student id: {request[0]}\nStudent name: {request[1]}\nTitle: {request[2]}\nAbstract: {request[3]}\nKeyword: {request[4]}\nDate: {request[8]}", font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx= 15, pady=7)


            student_id_label = tk.Label(thesis_defense_request_frame, text="Student id:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            student_id_label.place(x=65, y=319)
            student_id_entry = tk.Entry(thesis_defense_request_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            student_id_entry.place(x=140, y=310, width=ENTRY_WIDTH, height=ENTRY_HEIGHT)

            combo = ttk.Combobox(thesis_defense_request_frame, values=["accept", "reject"], state="readonly", style="Custom.TCombobox")
            combo.current(0)
            combo.place(x=460, y=310, width=70, height=40)

            def open_pdf_btn_action():
                if student_id_entry.get() == "":
                    warn_label = tk.Label(thesis_defense_request_frame, text="student id must not empty.", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                    warn_label.place(x=65, y=560)
                else:
                    student_id = int(student_id_entry.get().strip())
                    flag = False
                    for request in request_list:
                        if request[0] == student_id:
                            flag = True
                            file = FileManager(request[5])
                            file.open_file()
                            break
                    if not flag:
                        warn_label = tk.Label(thesis_defense_request_frame, text="There is no student with this id.", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                        warn_label.place(x=65, y=560)


            open_pdf_btn = tk.Button(thesis_defense_request_frame, text="Open pdf", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=open_pdf_btn_action)
            open_pdf_btn.place(x=140, y=370, width=80, height=40)

            def open_first_page_btn_action():
                if student_id_entry.get() == "":
                    warn_label = tk.Label(thesis_defense_request_frame, text="student id must not empty.", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                    warn_label.place(x=65, y=560)
                else:
                    student_id = int(student_id_entry.get().strip())
                    flag = False
                    for request in request_list:
                        if request[0] == student_id:
                            flag = True
                            file = FileManager(request[6])
                            file.open_file()
                            break
                    if not flag:
                        warn_label = tk.Label(thesis_defense_request_frame, text="There is no student with this id.", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                        warn_label.place(x=65, y=560)


            open_first_page_btn = tk.Button(thesis_defense_request_frame, text="Open first page", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=open_first_page_btn_action)
            open_first_page_btn.place(x=240, y=370, width=120, height=40)

            def open_last_page_btn_action():
                if student_id_entry.get() == "":
                    warn_label = tk.Label(thesis_defense_request_frame, text="student id must not empty.", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                    warn_label.place(x=65, y=560)
                else:
                    student_id = int(student_id_entry.get().strip())
                    flag = False
                    for request in request_list:
                        if request[0] == student_id:
                            flag = True
                            file = FileManager(request[7])
                            file.open_file()
                            break
                    if not flag:
                        warn_label = tk.Label(thesis_defense_request_frame, text="There is no student with this id.", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                        warn_label.place(x=65, y=560)

            open_last_page_btn = tk.Button(thesis_defense_request_frame, text="Open last page", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=open_last_page_btn_action)
            open_last_page_btn.place(x=380, y=370, width=120, height=40)

            internal_examiner_id_label = tk.Label(thesis_defense_request_frame, text="Internal examiner id:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            internal_examiner_id_label.place(x=65, y=445)
            internal_examiner_id_entry = tk.Entry(thesis_defense_request_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            internal_examiner_id_entry.place(x=205, y=436, width=70, height=ENTRY_HEIGHT)

            external_examiner_name_label = tk.Label(thesis_defense_request_frame, text="External examiner name:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            external_examiner_name_label.place(x=320, y=445)
            external_examiner_name_entry = tk.Entry(thesis_defense_request_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            external_examiner_name_entry.place(x=490, y=436, width=150, height=ENTRY_HEIGHT)

            date_label = tk.Label(thesis_defense_request_frame, text="Date:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            date_label.place(x=65, y=500)
            date_entry = tk.Entry(thesis_defense_request_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            date_entry.place(x=110, y=491, width=165, height=ENTRY_HEIGHT)

            date_label = tk.Label(thesis_defense_request_frame, text="example: 17/08/2025", font=("Arial", 9), bg=RIGHT_COLOR, fg="white")
            date_label.place(x=280, y=500)


            def submit_btn_action():
                student_id = student_id_entry.get().strip()
                internal_examiner_id = internal_examiner_id_entry.get().strip()
                external_examiner_name = external_examiner_name_entry.get().strip()
                date = date_entry.get().strip()

                decision = True
                if combo.get() == "reject":
                    decision = False
                    message = master_object.thesis_defense_decision(student_id, decision)
                else:
                    message = master_object.thesis_defense_decision(student_id, decision, internal_examiner_id, external_examiner_name, date)

                message_label = tk.Label(thesis_defense_request_frame, text=message, font=("Arial", 11), bg=RIGHT_COLOR,fg="white")
                message_label.place(x=65, y=570)

            submit_btn = tk.Button(thesis_defense_request_frame, text="Submit", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=submit_btn_action)
            submit_btn.place(x=420, y=550, width=228, height=60)

        thesis_defense_request_btn = tk.Button(left_frame, text="Thesis defense requests", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=thesis_defense_request_btn_action)
        thesis_defense_request_btn.place(x=0, y=322, width=228, height=60)

        line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        line_between.place(x=0, y=382)

        def register_thesis_defense_grade_btn_action():
            thesis_request_frame.place_forget()
            thesis_defense_request_frame.place_forget()
            register_external_examiner_grade_frame.place_forget()
            theses_bank_frame.place_forget()
            register_thesis_defense_grade_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            register_thesis_defense_grade_btn.config(bg=RIGHT_COLOR)
            thesis_request_btn.config(bg=BTN_COLOR)
            thesis_defense_request_btn.config(bg=BTN_COLOR)
            register_external_examiner_grade_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)

            canvas = tk.Canvas(register_thesis_defense_grade_frame, bg=RIGHT_COLOR, highlightthickness=0, width=600, height=300)
            scrollbar = tk.Scrollbar(register_thesis_defense_grade_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=RIGHT_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.place(x=20, y=20, width=620, height=350)
            scrollbar.place(x=670, y=20, width=15, height=350)

            request_list = master_object.internal_examiner_defenses_print()
            for request in request_list:
                tk.Label(scrollable_frame, width=90,
                         text=f"Defense id: {request[0]}\nStudent id: {request[1]}\nStudent name: {request[2]}\nExaminers name: {request[3]}",
                         font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx=15, pady=7)

            student_id_label = tk.Label(register_thesis_defense_grade_frame, text="Student id:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            student_id_label.place(x=65, y=399)
            student_id_entry = tk.Entry(register_thesis_defense_grade_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            student_id_entry.place(x=145, y=390, width=200, height=ENTRY_HEIGHT)

            grade_label = tk.Label(register_thesis_defense_grade_frame, text="Grade:", font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
            grade_label.place(x=385, y=399)
            grade_entry = tk.Entry(register_thesis_defense_grade_frame, bg=INPUT_COLOR, insertbackground="white", font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            grade_entry.place(x=440, y=390, width=200, height=ENTRY_HEIGHT)

            def submit_btn_action():
                student_id = student_id_entry.get().strip()
                grade = grade_entry.get().strip()
                message = master_object.register_thesis_defense_grade_internal(student_id, grade)

                message_label = tk.Label(register_thesis_defense_grade_frame, text=message, font=("Arial", 11), bg=RIGHT_COLOR,
                                         fg="white")
                message_label.place(x=65, y=520)

            submit_btn = tk.Button(register_thesis_defense_grade_frame, text="Submit", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=submit_btn_action)
            submit_btn.place(x=420, y=500, width=228, height=60)

        register_thesis_defense_grade_btn = tk.Button(left_frame, text="Register thesis defense grade", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=register_thesis_defense_grade_btn_action)
        register_thesis_defense_grade_btn.place(x=0, y=384, width=228, height=60)

        line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        line_between.place(x=0, y=444)

        def register_external_examiner_grade_btn_action():
            thesis_request_frame.place_forget()
            thesis_defense_request_frame.place_forget()
            register_thesis_defense_grade_frame.place_forget()
            theses_bank_frame.place_forget()
            register_external_examiner_grade_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            register_external_examiner_grade_btn.config(bg=RIGHT_COLOR)
            thesis_request_btn.config(bg=BTN_COLOR)
            thesis_defense_request_btn.config(bg=BTN_COLOR)
            register_thesis_defense_grade_btn.config(bg=BTN_COLOR)
            theses_bank_btn.config(bg=BTN_COLOR)

            canvas = tk.Canvas(register_external_examiner_grade_frame, bg=RIGHT_COLOR, highlightthickness=0, width=600,
                               height=300)
            scrollbar = tk.Scrollbar(register_external_examiner_grade_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=RIGHT_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.place(x=20, y=20, width=620, height=350)
            scrollbar.place(x=670, y=20, width=15, height=350)

            request_list = master_object.external_examiner_defenses_print()
            for request in request_list:
                tk.Label(scrollable_frame, width=90,
                         text=f"Defense id: {request[0]}\nStudent id: {request[1]}\nStudent name: {request[2]}\nExaminers name: {request[3]}",
                         font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx=15, pady=7)

            student_id_label = tk.Label(register_external_examiner_grade_frame, text="Student id:", font=("Arial", 11),
                                        bg=RIGHT_COLOR, fg="white")
            student_id_label.place(x=65, y=399)
            student_id_entry = tk.Entry(register_external_examiner_grade_frame, bg=INPUT_COLOR, insertbackground="white",
                                        font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            student_id_entry.place(x=145, y=390, width=200, height=ENTRY_HEIGHT)

            grade_label = tk.Label(register_external_examiner_grade_frame, text="Grade:", font=("Arial", 11),
                                   bg=RIGHT_COLOR, fg="white")
            grade_label.place(x=385, y=399)
            grade_entry = tk.Entry(register_external_examiner_grade_frame, bg=INPUT_COLOR, insertbackground="white",
                                   font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            grade_entry.place(x=440, y=390, width=200, height=ENTRY_HEIGHT)

            def submit_btn_action():
                student_id = student_id_entry.get().strip()
                grade = grade_entry.get().strip()
                message = master_object.register_thesis_defense_grade_external(student_id, grade)

                message_label = tk.Label(register_external_examiner_grade_frame, text=message, font=("Arial", 11),
                                         bg=RIGHT_COLOR,
                                         fg="white")
                message_label.place(x=65, y=520)

            submit_btn = tk.Button(register_external_examiner_grade_frame, text="Submit", font=("Arial", 11), bg=BTN_COLOR,
                                   fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2",
                                   command=submit_btn_action)
            submit_btn.place(x=420, y=500, width=228, height=60)

        register_external_examiner_grade_btn = tk.Button(left_frame, text="Register external examiner grade", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=register_external_examiner_grade_btn_action)
        register_external_examiner_grade_btn.place(x=0, y=446, width=228, height=60)

        line_between = tk.Canvas(left_frame, width=230, height=2, bg=LINE_COLOR, highlightthickness=0)
        line_between.place(x=0, y=506)

        def theses_bank_btn_action():
            thesis_request_frame.place_forget()
            thesis_defense_request_frame.place_forget()
            register_thesis_defense_grade_frame.place_forget()
            register_external_examiner_grade_frame.place_forget()
            theses_bank_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)
            theses_bank_btn.config(bg=RIGHT_COLOR)
            thesis_request_btn.config(bg=BTN_COLOR)
            thesis_defense_request_btn.config(bg=BTN_COLOR)
            register_thesis_defense_grade_btn.config(bg=BTN_COLOR)
            register_external_examiner_grade_btn.config(bg=BTN_COLOR)

            canvas = tk.Canvas(theses_bank_frame, bg=RIGHT_COLOR, highlightthickness=0, width=600,
                               height=300)
            scrollbar = tk.Scrollbar(theses_bank_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=RIGHT_COLOR)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.place(x=20, y=20, width=620, height=350)
            scrollbar.place(x=670, y=20, width=15, height=350)

            defenses_list = ThesisSearch("", "", "", "", "", "").print_all()
            for defense in defenses_list:
                tk.Label(scrollable_frame, width=90,
                         text=f"Title: {defense[0]}\nAbstract: {defense[1]}\nKeywords: {defense[2]}\nAuthor id: {defense[3]}\nAuthor: {defense[4]}\ndate: {defense[5]}\nexaminers: {defense[6]}\nmaster: {defense[7]}\nscore: {defense[8]}",
                         font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx=15,
                                                                                                        pady=7)

            title_label = tk.Label(theses_bank_frame, text="Title:", font=("Arial", 11),
                                        bg=RIGHT_COLOR, fg="white")
            title_label.place(x=15, y=399)
            title_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR,
                                        insertbackground="white",
                                        font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            title_entry.place(x=55, y=390, width=140, height=ENTRY_HEIGHT)

            master_name_label = tk.Label(theses_bank_frame, text="Master name:", font=("Arial", 11),
                                   bg=RIGHT_COLOR, fg="white")
            master_name_label.place(x=220, y=399)
            master_name_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                   font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            master_name_entry.place(x=320, y=390, width=140, height=ENTRY_HEIGHT)

            keyword_label = tk.Label(theses_bank_frame, text="Keyword:", font=("Arial", 11),
                                         bg=RIGHT_COLOR, fg="white")
            keyword_label.place(x=485, y=399)
            keyword_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                         font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            keyword_entry.place(x=555, y=390, width=140, height=ENTRY_HEIGHT)

            author_label = tk.Label(theses_bank_frame, text="Author:", font=("Arial", 11),
                                     bg=RIGHT_COLOR, fg="white")
            author_label.place(x=15, y=467)
            author_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                     font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            author_entry.place(x=70, y=460, width=140, height=ENTRY_HEIGHT)

            year_label = tk.Label(theses_bank_frame, text="Year:", font=("Arial", 11),
                                    bg=RIGHT_COLOR, fg="white")
            year_label.place(x=230, y=467)
            year_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                    font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            year_entry.place(x=275, y=460, width=140, height=ENTRY_HEIGHT)

            examiner_label = tk.Label(theses_bank_frame, text="Examiner:", font=("Arial", 11),
                                  bg=RIGHT_COLOR, fg="white")
            examiner_label.place(x=440, y=467)
            examiner_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                  font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            examiner_entry.place(x=520, y=460, width=140, height=ENTRY_HEIGHT)

            author_id_label = tk.Label(theses_bank_frame, text="Author id:", font=("Arial", 11),
                                      bg=RIGHT_COLOR, fg="white")
            author_id_label.place(x=15, y=567)
            author_id_entry = tk.Entry(theses_bank_frame, bg=INPUT_COLOR, insertbackground="white",
                                      font=("Arial", 11), fg="white", bd=0, highlightthickness=0)
            author_id_entry.place(x=85, y=560, width=100, height=ENTRY_HEIGHT)

            def open_pdf_btn_action():
                if author_id_entry.get() == "":
                    warn_label = tk.Label(theses_bank_frame, text="author id must not empty.",
                                          font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                    warn_label.place(x=15, y=610)
                else:
                    author_id = int(author_id_entry.get().strip())
                    flag = False
                    for defense in defenses_list:
                        if defense[3] == author_id:
                            flag = True
                            file = FileManager(defense[9])
                            file.open_file()
                            break
                    if not flag:
                        warn_label = tk.Label(theses_bank_frame, text="There is no author with this id.",
                                              font=("Arial", 11), bg=RIGHT_COLOR, fg="white")
                        warn_label.place(x=15, y=610)

            open_pdf_btn = tk.Button(theses_bank_frame, text="Open pdf", font=("Arial", 11),
                                   bg=BTN_COLOR,
                                   fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2",
                                   command=open_pdf_btn_action)
            open_pdf_btn.place(x=200, y=560, width=100, height=ENTRY_HEIGHT)

            def search_btn_action():
                for widget in scrollable_frame.winfo_children():
                    widget.destroy()
                title = title_entry.get().strip()
                master_name = master_name_entry.get().strip()
                keyword = keyword_entry.get().strip()
                author = author_entry.get().strip()
                year = year_entry.get().strip()
                examiner = examiner_entry.get().strip()

                defenses_list = ThesisSearch(title, master_name, keyword, author, year, examiner).search()
                for defense in defenses_list:
                    tk.Label(scrollable_frame, width=90,
                             text=f"Title: {defense[0]}\nAbstract: {defense[1]}\nKeywords: {defense[2]}\nAuthor id: {defense[3]}\nAuthor: {defense[4]}\ndate: {defense[5]}\nexaminers: {defense[6]}\nmaster: {defense[7]}\nscore: {defense[8]}",
                             font=("Arial", 9), anchor="w", bg=LEFT_COLOR, fg="white", justify="left").pack(padx=15,
                                                                                                            pady=7)

            search_btn = tk.Button(theses_bank_frame, text="Search", font=("Arial", 11),
                                   bg=BTN_COLOR,
                                   fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2",
                                   command=search_btn_action)
            search_btn.place(x=420, y=550, width=228, height=60)

        theses_bank_btn = tk.Button(left_frame, text="Theses Bank", font=("Arial", 11), bg=BTN_COLOR, fg="white", bd=0, highlightthickness=0, activebackground="#ADD8E6", cursor="hand2", command=theses_bank_btn_action)
        theses_bank_btn.place(x=0, y=508, width=228, height=60)


        # -----------------------right frames--------------------------------
        right_frame = tk.Frame(master_form, bg=RIGHT_COLOR)
        right_frame.place(x=230, y=0, width=WIDTH - 230, height=HEIGHT)

        thesis_request_frame = tk.Frame(master_form, bg=RIGHT_COLOR)

        thesis_defense_request_frame = tk.Frame(master_form, bg=RIGHT_COLOR)

        register_thesis_defense_grade_frame = tk.Frame(master_form, bg=RIGHT_COLOR)

        register_external_examiner_grade_frame = tk.Frame(master_form, bg=RIGHT_COLOR)

        theses_bank_frame = tk.Frame(master_form, bg=RIGHT_COLOR)
