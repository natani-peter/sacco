import customtkinter as ctk
import mysql.connector
import bcrypt
from tkinter import messagebox as box
from register import Register
from widgets import EntryWidget, ButtonWidget
from settings import *

from dashboard import Dashboard


class LogIn(ctk.CTkFrame):
    """ creates the log in interface"""

    def __init__(self, parent):
        super(LogIn, self).__init__(parent, fg_color='#efc')
        self.parent = parent
        self.parent.geometry('350x450')
        self.pack(expand=True, fill='both', padx=25, pady=10)
        ctk.CTkLabel(self, text='LOG INTO YOUR ACCOUNT', text_color='#000', font=('sans-serif', 20, 'bold')) \
            .pack(pady=40)

        self.phone = EntryWidget(self, 'Enter Your Phone')
        self.phone.pack(padx=30, fill='x', pady=5)

        self.pin = EntryWidget(self, 'Enter Your Pin')
        self.pin.configure(show='*')
        self.pin.pack(padx=30, fill='x', pady=30)

        self.login_button = ButtonWidget(self, self.login, 'LOG IN')
        self.login_button.pack(padx=30, fill='x', pady=0)

        self.show_button = ctk.CTkButton(self.pin, text='SHOW', command=self.toggle, width=30, fg_color=blue,
                                         height=25)
        self.show_button.place(relx=0.98, rely=0.1, anchor='ne')

        ctk.CTkLabel(self, text='Have no account?', text_color='#000').place(x=150, y=310, anchor='ne')
        self.register_button = ButtonWidget(self, self.reg, 'Register')
        self.register_button.place(x=150, y=315, anchor='nw')

        self.register_button.configure(fg_color='#efc', hover_color='#efc', text_color=blue, height=0, width=0)

    def toggle(self):
        """ Changes the visibility of the password"""
        current_state = self.pin.cget('show')

        if current_state == '*':
            self.pin.configure(show='')
            self.show_button.configure(text='HIDE')
        else:
            self.pin.configure(show='*')
            self.show_button.configure(text='SHOW')

    def reg(self):
        """ Brings the register frame"""

        self.pack_forget()
        Register(self.parent, self.bring)

    def bring(self):
        self.pack(expand=True, fill='both', padx=25, pady=10)

    def login(self):
        """ logs in the user into the system"""

        with mysql.connector.connect(host="localhost", user="root", password="@natan1_p373r.", database="sacco") \
                as connection:
            cursor = connection.cursor()

            phone = self.phone.get()
            pin = self.pin.get()
            if len(phone) != 10:
                box.showinfo('INFO', "phone number must be 10 digits \nWithout a space and begin with zero")
            else:

                retrieve_logger = '''SELECT pin FROM members WHERE phone_number = %s'''
                user_phone = (phone,)
                cursor.execute(retrieve_logger, user_phone)
                user = cursor.fetchone()
                if user:
                    database_password = user[0].encode()
                    if bcrypt.checkpw(pin.encode(), database_password):
                        obtain_name = '''select member_name,member_id from members where phone_number=%s'''
                        cursor.execute(obtain_name, user_phone)
                        results = cursor.fetchone()
                        user_name = results[0]
                        user_id = results[1]
                        self.pack_forget()
                        Dashboard(self.parent, user_name, user_id)
                    else:
                        box.showerror('ERROR', 'Invalid Pin')
                else:
                    box.showinfo('INFO', "User does not exist\nConsider Creating An Account")
