import customtkinter as ctk
from widgets import EntryWidget, ButtonWidget
from settings import *
import mysql.connector
from tkinter import messagebox as box
import bcrypt
from dashboard import Dashboard


class Register(ctk.CTkFrame):
    """creates the register frame for user registration"""

    def __init__(self, parent, func):
        super(Register, self).__init__(parent, fg_color='#efc')
        self.parent = parent
        self.parent.geometry('350x450')
        self.pack(expand=True, fill='both', padx=25, pady=10)
        self.func = func

        ctk.CTkLabel(self, text='REGISTER YOUR ACCOUNT', text_color='#000', font=('sans-serif', 20, 'bold')) \
            .pack(pady=30)

        self.name = EntryWidget(self, 'Enter Your Name')
        self.name.pack(padx=30, fill='x', pady=5)

        self.phone = EntryWidget(self, 'Enter Your Phone')
        self.phone.pack(padx=30, fill='x', pady=5)

        self.pin = EntryWidget(self, 'Enter Your Pin')
        self.pin.pack(padx=30, fill='x', pady=20)

        self.confirm_pin = EntryWidget(self, 'Confirm Your Pin')
        self.confirm_pin.pack(padx=30, fill='x', pady=0)

        self.register_button = ButtonWidget(self, self.enter, 'REGISTER')
        self.register_button.pack(padx=30, fill='x', pady=15)

        ctk.CTkLabel(self, text='Have account?', text_color='#000').place(x=200, y=380, anchor='ne')
        self.login_button = ButtonWidget(self, func, 'Log in')
        self.login_button.place(x=200, y=385, anchor='nw')

        self.login_button.configure(fg_color='#efc', hover_color='#efc', text_color=blue, height=0, width=0)

        self.login_button.bind('<Button-1>', self.kill)
        self.register_button.bind('<Button-1>', self.kill)

    def kill(self, event):
        self.pack_forget()
        return event

    def logout(self):
        self.pack_forget()
        self.func()

    def enter(self):
        """ registers the user"""
        with mysql.connector.connect(host="localhost", user="root", password="@natan1_p373r.", database="sacco") as \
                connection:
            cursor = connection.cursor()

            name = self.name.get()
            phone = self.phone.get()
            pin1 = self.pin.get()
            pin2 = self.confirm_pin.get()
            if len(name) <= 2:
                box.showinfo(title='INFO', message="\tname should be more than two characters")
            elif len(phone) != 10:
                box.showinfo(title='INFO',
                             message="\tphone number must be 10 digits\n\tWithout a space and begin with zero")
            elif pin1 != pin2:
                box.showinfo(title='info', message='Please Confirm Your Pin')
            elif len(pin1) != 5:
                box.showinfo(title='info', message='Pin must be five digits')

            try:
                assert not (phone.__contains__(" "))
            except AssertionError:
                box.showerror(title='ERROR', message='The phone number cant contain spaces')
            else:
                if pin1 == pin2:
                    salt = bcrypt.gensalt()
                    pin = bcrypt.hashpw(pin1.encode(), salt)
                    try:
                        enter_user_into_table = \
                            """INSERT INTO members (phone_number,pin,member_name) VALUES(%s,%s,%s)"""
                        member_data = (phone, pin, name)
                        cursor.execute(enter_user_into_table, member_data)
                        connection.commit()
                        box.showinfo(title='INFO', message="\tAccount created successfully")
                    except mysql.connector.IntegrityError:
                        box.showerror(title='ERROR', message="\tuser already exists!")
                    try:
                        wanted_id = ''' select member_id from members where phone_number = %s'''
                        user_got = (phone,)
                        cursor.execute(wanted_id, user_got)
                        passed_id = cursor.fetchone()[0]
                        enter_balance_into_table = '''INSERT INTO accounts (user_id, phone_number) VALUES (%s, %s)'''
                        user_balance = (passed_id, phone)
                        cursor.execute(enter_balance_into_table, user_balance)
                        connection.commit()
                        Dashboard(self.parent, self.logout, name)

                    except mysql.connector.IntegrityError:
                        Dashboard(self.parent, self.logout, name)
                else:
                    box.showinfo(title='info', message='Please Confirm Your Pin')
