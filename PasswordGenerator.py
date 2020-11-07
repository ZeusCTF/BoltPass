import secrets
import string
import sqlite3

print('Thank you for using BoltPass')
print("""
__
\ \\
 \ \\
__\ \\
\  __\\
 \ \\
__\ \\
\  __\\
 \ \\
  \ \\
   \/
""")
print('Please note, this should not be used to store any important information as this program is still being worked on')

total = []

def main():
    def continue2():
        x = input("Continue usage?  Enter 'y' or 'n': ")
        if x == 'y':
            main()
        elif x == 'n':
            print('Goodbye!')
        else:
            print('Bad Input')

    def build_library():
        for char in string.ascii_letters:
            total.append(char)
        for num in string.digits:
            total.append(num)
        for punc in string.punctuation:
            total.append(punc)
    build_library()

    def delete():
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        print('BE CAREFUL, THIS WILL DELETE EVERYTHING FROM AN ENTRY')
        print()
        x = input('Please enter the URL of the record to be deleted: ')
        c.execute("DELETE FROM passwords WHERE URL = '" + x +"'")
        conn.commit()
        continue2()

    def update():
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        print('Follow the steps to update your password')
        print()
        x = input('Enter the URL: ')
        print()
        updatedPass = input('Enter the updated password: ')
        c.execute("UPDATE passwords SET password = '" + updatedPass + "' WHERE URL = '" + x + "'")
        conn.commit()

    def genPasswd(x):
        numLength = int(x)
        Pass = ''
        while numLength != 0:
            numLength -= 1
            password = total[secrets.randbelow(94)]
            Pass += password
        print('*' * 50)
        print()
        print('Below is the generated password:')
        print(Pass)
        print()
        print('*' * 50)
        return Pass

    def display():
        conn = sqlite3.connect('data.db')

        c = conn.cursor()

        c.execute("SELECT * FROM passwords")
        items = c.fetchall()
        for item in items:
            print(item)
        continue2()

    def addLogin():
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        URL = input('Please enter the URL: ')
        username = input('Please enter the Username/Email: ')
        q = input("Enter 'g' or 'm' respectfully to generate a password or add one manually: ")
        if q == 'g':
            password = genPasswd(input('How long should the password be?: '))
        elif q == 'm':
            password = input('Please enter the Password: ')
        c.execute("INSERT INTO passwords(URL, username, password) VALUES(?,?,?)", (URL, username, password))
        conn.commit()
        conn.close()
        continue2()

    prompt = input("""If you would like to see current login information please type 'current'.
    If you would like to update information please type 'update'
    If you would like to add login information please type 'add'
    If you would like to delete login information please type 'delete'
    """)

    if prompt == 'add':
        addLogin()
    elif prompt == 'update':
        update()
    elif prompt == 'current':
        display()
    elif prompt == 'delete':
        delete()
    else:
        print('Bad input')
main()