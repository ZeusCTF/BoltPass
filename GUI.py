from tkinter import messagebox
import tkinter
from tkinter import *
import sqlite3
import secrets
import string
import os

total = [] 

def initalSetup():
    conn = sqlite3.connect('BoltPass.db')
    c = conn.cursor()

    c.execute("""CREATE TABLE passwords (
        URL TEXT,
        username TEXT,
        password TEXT 
    )""")
    conn.commit()
    conn.close

if os.path.isfile('BoltPass.db') == False:
    initalSetup()
else:
    pass

def build_library():
        for char in string.ascii_letters:
            total.append(char)
        for num in string.digits:
            total.append(num)
        for punc in string.punctuation:
            total.append(punc)
build_library()

class DeleteLogin:
    def __init__(self):
        self.main_window = tkinter.Tk()

        self.URL = tkinter.Label(self.main_window, text = 'Please enter the URL: ')
        self.url_entry = tkinter.Entry(self.main_window)
        self.delete_button = tkinter.Button(self.main_window, text = 'Delete', command=self.DeleteLogin)

        self.URL.pack()
        self.url_entry.pack()
        self.delete_button.pack()

    def DeleteLogin(self):
        conn = sqlite3.connect('BoltPass.db')
        c = conn.cursor()
        x = self.url_entry.get()
        c.execute("DELETE FROM passwords WHERE URL = '" + x +"'")
        conn.commit()
        tkinter.messagebox.showinfo('BoltPass', 'The account credentials have been deleted')


class UpdateLogin:
    def __init__(self):
        self.main_window = tkinter.Tk()

        self.URL = tkinter.Label(self.main_window, text = 'Please enter the URL: ')
        self.url_entry = tkinter.Entry(self.main_window)
        self.update_button = tkinter.Button(self.main_window, text = 'Update password', command=self.UpdateLogin)

        self.URL.pack()
        self.url_entry.pack()
        self.update_button.pack()
        tkinter.mainloop()


    def UpdateLogin(self):
        conn = sqlite3.connect('BoltPass.db')
        c = conn.cursor()
        x = self.url_entry.get()
        Pass = ''
        # So it looks like if "" gets passed into the new password, this will break the SQL statement (cont.)
        # In this case, it seems that the below code omits the "" and hasn't broken yet :)
        for i in range(15):
            if i != '"':
                Pass += total[secrets.randbelow(94)]
            else:
                pass

        # Obviously this would update the password for multiple accounts if the user has multiple accounts for any one URL (cont.)
        # Perhaps this could be solved by using both URL and Username?
        c.execute("UPDATE passwords SET password = ' " + Pass + "' WHERE URL = '" + x + "'")
        conn.commit()
        tkinter.messagebox.showinfo('BoltPass', 'The below password has been updated within the database for the indicated account' + '\n' + Pass)


class addLogin:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.URL = tkinter.Label(self.main_window, text = 'Please enter the URL: ')
        self.url_entry = tkinter.Entry(self.main_window)
        self.Username = tkinter.Label(self.main_window, text = 'Please enter the Username/Email: ')
        self.user_entry = tkinter.Entry(self.main_window)



        self.auto_button = tkinter.Button(self.main_window, text = 'Generate password', command=self.AutoLogin)

        #pack everything
        self.Username.pack()
        self.user_entry.pack()
        self.URL.pack()
        self.url_entry.pack()
        self.auto_button.pack()
        
        
        
        tkinter.mainloop()
        

    
    def AutoLogin(self):
        Pass = ''
        for i in range(15):
            Pass += total[secrets.randbelow(94)]
        conn = sqlite3.connect('BoltPass.db')
        c = conn.cursor()
        c.execute("INSERT INTO passwords(URL, username, password) VALUES(?,?,?)", (self.url_entry.get(), self.user_entry.get(), Pass))
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo('BoltPass', 'The below password has been added to the database for the indicated account' + '\n' + Pass)

class DisplayGUI:
    def __init__(self, content):
        self.main_window = tkinter.Tk()
        self.Label = tkinter.Label(self.main_window, text = 'Thank you for using Bolt Pass! \n See below for a list of your credentials:\n' + content )
        self.Label.pack()
        tkinter.mainloop()

class InitialGUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.main_window.title('Bolt Pass')

        #button creation
        self.display_button = tkinter.Button(self.main_window, text = 'Display Credentials', command=self.display_option)
        self.delete_button = tkinter.Button(self.main_window, text = 'Delete Credentials', command=self.delete_option)
        self.update_button = tkinter.Button(self.main_window, text = 'Update Credentials', command=self.update_option)
        self.add_button = tkinter.Button(self.main_window, text = 'Add Credentials', command=self.add_option)

        #pack the buttons
        self.display_button.pack()
        self.delete_button.pack()
        self.update_button.pack()
        self.add_button.pack()
        
        tkinter.mainloop()
    
    def display_option(self):
        conn = sqlite3.connect('BoltPass.db')

        c = conn.cursor()

        c.execute("SELECT * FROM passwords")
        items = c.fetchall()
        with open('BoltPass.txt', 'w') as f:
            for item in items:
                f.write(str(item) + '\n')
        f.close()
        # Super complicated way to read/display all the passwords
        with open('BoltPass.txt', 'r') as f:
            z = f.readlines()
        string = ''
        for i in z:
            string += i + '\n'
        x = DisplayGUI(string)
        f.close()
        # This line removes the file created after all windows are closed, this helps with security (cont.)
        # But is really only a band-aid solution for the problem
        os.remove('BoltPass.txt')

    def add_option(self):
        add = addLogin()

    def update_option(self):
        update = UpdateLogin()

    def delete_option(self):
        delete = DeleteLogin()

start = InitialGUI()