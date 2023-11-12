import tkinter as tk
from datetime import datetime, time
from tkinter import ttk, messagebox as box

import customtkinter as ctk
import mysql.connector

from settings import *
from widgets import DashButtonWidget, EntryWidget, ButtonWidget


class Dashboard(ctk.CTkFrame):
    """
    This class handles the user activities of deposit, withdraw, check balance and his transaction history
    the deposit and withdrawing will be done by a number that was used during registration
    """

    def __init__(self, parent, current_user, user_id):
        super(Dashboard, self).__init__(master=parent, fg_color='#fef')
        self.table = None
        self.history_table = None
        self.deposit_amount = None
        self.down = None
        self.withdraw_amount = None
        self.top = None
        self.current_time = datetime.now().time()
        self.current_date = datetime.now().date().strftime('%d/%m/%Y')
        self.user_id = (user_id,)
        self.parent = parent
        self.parent.geometry('400x400+1100+100')
        self.parent.title('DASHBOARD')
        self.user = current_user
        self.title = ctk.CTkLabel(self, text='STAHIKA STAFF SACCO', text_color='black', font=font)
        self.title.place(relx=0.5, rely=0.1, anchor='center')

        self.greeting = ctk.CTkLabel(self, text=f'Hello {self.user.title()}', text_color='#456', font=font)
        self.greeting.place(relx=0.05, rely=0.2, anchor='nw')
        self.greet_user()

        self.drop()
        self.balance_ = DashButtonWidget(self, 'SAVINGS\n\n', self.balance, red, 150)
        self.balance_.place(rely=0.4, relx=0.05, anchor='nw')
        self.balance_.configure(text_color="#fff", font=font, hover_color=red)
        self.balance()

        self.deposit_btn = DashButtonWidget(self, 'DEPOSIT', self.deposit, green, 150, 80)
        self.deposit_btn.place(rely=0.4, relx=0.95, anchor='ne')
        self.deposit_btn.configure(font=font, text_color='#111', hover_color=light_green)

        self.withdraw_btn = DashButtonWidget(self, 'WITHDRAW', self.withdraw, dark_button_blue, 150, 80)
        self.withdraw_btn.place(rely=0.95, relx=0.05, anchor='sw')
        self.withdraw_btn.configure(font=font, text_color='#111', hover_color=button_blue)

        self.history_btn = DashButtonWidget(self, 'TRANSACTION\n\nHISTORY', self.history, dark_yellow, 150, 80)
        self.history_btn.place(rely=0.95, relx=0.95, anchor='se')
        self.history_btn.configure(font=font, text_color='#111', hover_color=yellow)

        self.pack(expand=True, fill='both', padx=10, pady=20)

    def greet_user(self):
        current_time = self.current_time
        if current_time < time(12, 0):
            self.greeting.configure(text=f'Good Morning {self.user.title()}')
        elif current_time < time(18, 0):
            self.greeting.configure(text=f'Good Afternoon {self.user.title()}')
        else:
            self.greeting.configure(text=f'Good Evening {self.user.title()}')

    def balance(self):
        with mysql.connector.connect(host='localhost', user='root', password='@natan1_p373r.',
                                     database='sacco') as conn:
            cursor = conn.cursor()
            obtain = ''' select balance from accounts where user_id= %s'''
            cursor.execute(obtain, self.user_id)
            balance = cursor.fetchone()[0]
            self.balance_.configure(text=f"SAVINGS\n\n{balance}")

    def drop(self):
        """A dropdown of  User's information """
        with mysql.connector.connect(host='localhost', user='root', password='@natan1_p373r.', database='sacco') as \
                connection:
            cursor = connection.cursor()
            obtain_details = '''select member_id, member_name, phone_number from members where member_id = %s'''
            cursor.execute(obtain_details, self.user_id)
            details = cursor.fetchone()
            user_id = details[0]
            name = details[1]
            number = details[2]

        user = ttk.Menubutton(self, text=f'YOUR INFO')
        dropdown = tk.Menu(user, tearoff=False)
        dropdown.add_cascade(label=f'USER ID: T/{1000 + int(user_id)}')
        dropdown.add_cascade(label=f'NAME: {name.upper()}')
        dropdown.add_cascade(label=f'PHONE: 0{number}')
        user.place(rely=0.2, relx=0.95, anchor='ne')
        user.configure(menu=dropdown)

    def deposit(self):
        """Handling user depositing into sacco"""
        self.down = ctk.CTkToplevel(fg_color='#fff')
        self.down.title('DEPOSIT SAVINGS')
        self.title = ctk.CTkLabel(self.down, text='STAHIKA STAFF SACCO', text_color='black', font=font)
        self.title.place(relx=0.5, rely=0.2, anchor='center')
        # self.down.attributes('-topmost', 1)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        widget_width = 400
        widget_height = 150
        self.down.geometry(f'{widget_width}x{widget_height}+{int((screen_width - widget_width) / 2)}+'
                           f'{(int(screen_height - widget_height)) / 2}')

        self.deposit_amount = EntryWidget(self.down, 'Enter Amount')
        self.deposit_amount.configure(width=300)
        self.deposit_amount.place(relx=0.5, rely=0.5, anchor='center')

        okay = ButtonWidget(self.down, lambda: self.handle_all('deposit', self.down), 'OK', 30, 30)
        okay.place(rely=0.8, relx=0.3, anchor='center')

        cancel_ = ButtonWidget(self.down, lambda: self.cancel('down'), 'CANCEL', 30, 40)
        cancel_.place(rely=0.8, relx=0.7, anchor='center')

    def withdraw(self):
        """handling withdrawing from the sacco"""
        self.top = ctk.CTkToplevel(fg_color='#fff')
        self.top.title('WITHDRAW SAVINGS')
        self.title = ctk.CTkLabel(self.top, text='STAHIKA STAFF SACCO', text_color='black', font=font)
        self.title.place(relx=0.5, rely=0.2, anchor='center')
        # self.top.attributes('-topmost',0.5)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        widget_width = 400
        widget_height = 150
        self.top.geometry(f'{widget_width}x{widget_height}+{int((screen_width - widget_width) / 2)}+'
                          f'{(int(screen_height - widget_height)) / 2}')

        self.withdraw_amount = EntryWidget(self.top, 'Enter Amount')
        self.withdraw_amount.configure(width=300)
        self.withdraw_amount.place(relx=0.5, rely=0.5, anchor='center')

        okay = ButtonWidget(self.top, lambda: self.handle_all('withdraw', self.top), 'OK', 30, 30)
        okay.place(rely=0.8, relx=0.3, anchor='center')

        cancel = ButtonWidget(self.top, lambda: self.cancel('top'), 'CANCEL', 30, 40)
        cancel.place(rely=0.8, relx=0.7, anchor='center')

    def cancel(self, message):
        if message == 'top':
            self.top.destroy()
        elif message == 'down':
            self.down.destroy()

    def handle_all(self, action, master):
        """ with this function we will handle all the depositing and withdrawing"""
        if action == 'withdraw':
            amount = int(self.withdraw_amount.get())
            if amount:
                if amount < 500:
                    box.showinfo('INFO', 'Minimum Withdraw Amount is 500')
                else:
                    with mysql.connector.connect(host='localhost', user='root', password='@natan1_p373r.',
                                                 database='sacco') as connection:
                        cursor = connection.cursor()

                        balance_query = ''' select balance from accounts where user_id = %s'''
                        cursor.execute(balance_query, self.user_id)
                        current_balance = int(cursor.fetchone()[0])

                        if current_balance < amount:
                            box.showinfo('INFO', 'insufficient Account balance')
                        else:
                            new_balance = current_balance - amount

                            # update the new balance
                            record1 = ''' update accounts set balance = %s where user_id = %s'''
                            cursor.execute(record1, (new_balance, self.user_id[0]))
                            connection.commit()

                            # record the transaction
                            record2 = '''insert into transactions (user_id,date_of_the_day,action_done,amount,balance) 
                            values (%s,%s,%s,%s,%s)'''
                            records = (self.user_id[0], self.current_date, action, amount, new_balance)
                            cursor.execute(record2, records)
                            connection.commit()

                            # give feedback

                            transaction_id_query = ''' select max(transaction_id) from transactions'''
                            cursor.execute(transaction_id_query)
                            transaction_id = cursor.fetchone()[0]
                            box.showinfo(title='INFO', message=f"Cash {action.title()} of UGX. {amount}.\n"
                                                               f"Your new balance is UGX. {new_balance},\n"
                                                               f"Transaction ID: 000{transaction_id}\n"
                                                               f"{self.current_date} "
                                                               f"{self.current_time.strftime('%H:%M')}")
                    self.balance()
                    master.destroy()

            else:
                box.showerror(title='ERROR', message=f"Enter amount Please")

        elif action == 'deposit':
            amount = int(self.deposit_amount.get())
            if amount:
                with mysql.connector.connect(host='localhost', user='root', password='@natan1_p373r.',
                                             database='sacco') as conn:
                    cursor = conn.cursor()
                    obtain = ''' select balance from accounts where user_id = %s'''
                    cursor.execute(obtain, self.user_id)
                    user_balance = cursor.fetchone()[0]

                    if amount < 999:
                        box.showinfo('INFO', 'Minimum deposit is UGX. 1000')
                    else:
                        new_balance = amount + user_balance

                        record1 = '''update accounts set balance = %s where user_id = %s '''
                        cursor.execute(record1, (new_balance, self.user_id[0]))
                        conn.commit()

                        record2 = """insert into transactions (user_id,
                                   date_of_the_day,action_done,amount,balance) values (%s,%s,%s,%s,%s)"""
                        transaction = (self.user_id[0], self.current_date, action, amount, new_balance)
                        cursor.execute(record2, transaction)
                        conn.commit()

                        max_id = """select max(transaction_id) from transactions"""
                        cursor.execute(max_id)
                        transaction_id = cursor.fetchone()[0]

                        box.showinfo(title='INFO', message=f"Cash {action.title()} of UGX. {amount}.\n"
                                                           f"Your new balance is UGX. {new_balance},\n"
                                                           f"Transaction ID: 000{transaction_id}\n"
                                                           f"{self.current_date} "
                                                           f"{self.current_time.strftime('%H:%M')}")

                        self.balance()
                        master.destroy()
            else:
                box.showerror(title='ERROR', message=f"Enter amount Please")

    def history(self):
        """ Fetch user's transaction history"""

        with mysql.connector.connect(host='localhost', user='root', password='@natan1_p373r.',
                                     database='sacco') as connection:
            cursor = connection.cursor()
            history_query = ''' select * from transactions where user_id = %s'''
            cursor.execute(history_query, self.user_id)
            results = cursor.fetchall()

        self.history_table = ctk.CTkToplevel(fg_color='#eee')
        self.history_table.title('TRANSACTION HISTORY')
        self.history_table.geometry('800x300+0+0')

        self.table = ttk.Treeview(self.history_table, columns=('0', '1', '2', '3'), show='headings', padding=3)
        self.table.heading('0', text='DATE')
        self.table.heading('1', text='ACTION')
        self.table.heading('2', text='AMOUNT')
        self.table.heading('3', text='BALANCE')

        for result in results:
            date = result[1]
            action = result[2].title()
            amount = result[3]
            balance = result[4]
            self.table.insert(parent='', index=0, values=(date, action, amount, balance))

        self.table.pack(expand=True, fill='both')
