import customtkinter as ctk
from settings import *
from widgets import ButtonWidget
from login import LogIn
from register import Register


class App(ctk.CTk):
    def __init__(self):
        """ The main app that runs at first"""
        super(App, self).__init__(fg_color=blue)
        self.geometry('350x400+1000+200')
        self.title('STAFF SACCO')
        self.resizable(False, False)

        self.login = lambda: LogIn(self)
        self.register = lambda: Register(self, self.login)

        self.frame = ctk.CTkFrame(self, fg_color='#fff')
        self.frame.pack(expand=True, fill='both', padx=10, pady=15)
        ctk.CTkLabel(self.frame, text='WELCOME TO \n\nSTAHIKA STAFF SACCO', text_color='#000', font=('sans-serif', 24,
                                                                                                     'bold')) \
            .pack(pady=20, padx=5)

        log = ButtonWidget(self.frame, self.login, 'LOG IN', 80, 250)
        log.place(x=150, y=190, anchor='center')
        log.configure(fg_color=dark_button_blue, hover_color=button_blue, font=('sans-serif', 20))

        log.bind('<Button-1>', self.kill)

        reg = ButtonWidget(self.frame, self.register, 'REGISTER', 80, 250)
        reg.place(x=150, y=300, anchor='center')
        reg.configure(fg_color=dark_red, hover_color=red, font=('sans-serif', 20))
        reg.bind('<Button-1>', self.kill)
        self.mainloop()

    def kill(self, event):
        self.frame.pack_forget()


if __name__ == '__main__':
    App()
