import sqlite3
from sqlite3 import Error
import random
import time
import string
import pyperclip
from datetime import datetime
import re


def main():

    # establishing a new sqlite db connection
    conn = sqlite3.connect('v1.db')
    c = conn.cursor()

    # table SCHEME:
    # columns:
    # Name of service
    # mail
    # Password
    # date of entering the db

    qr = ''' CREATE TABLE IF NOT EXISTS info(
        appName TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        pass TEXT NOT NULL,
        inDate TEXT
        )'''

    c.execute(qr)
    conn.commit()

    def get_ctd():
        now = datetime.now()
        dt = str(now.strftime('%Y-%m-%d %H:%M:%S'))
        return dt

#  creating a random password with a password generator function.
    def random_pass():
        specials = '!@#$%&'
        chars = string.ascii_letters + string.digits + specials
        password = ''.join(random.choice(chars) for _ in range(int(12)))
        print('Password generated: {0}'.format(password))
        return password

# Checks if the mail is valid and comply to the standards

    def mail_check(mail):
        if re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", mail):
            return True
        return False


#  inset a new password for a new account.

    def insert(app, mail, p):
        with conn:
            try:
                c.execute("INSERT INTO info VALUES (?, ?, ?, ?)",
                          (app, mail, p, get_ctd()))
                print('Your info has been succesfuly added to the VAULT.')

            except Error as e:
                print(f'error {e} occured')

#  get a password by name of service/acount name (will be copied to clipboard).
    def get_pass(app):
        c.execute("SELECT * FROM info WHERE appName=?", (app,))
        data = list(c.fetchone())
        print('For your {0} account, you used this email: {1}, your password is: {2} was last updated on {3}'.format(
            data[0].title(), data[1], data[2], data[3]))
        pyperclip.copy(data[2])

    def update_pass(app, np):
        with conn:
            c.execute(
                "UPDATE info SET pass=(?), inDate=(?) WHERE appName=(?)", (np, get_ctd(), app))
            print(
                'Your password to {0} has now changed to: {1}'.format(app, np))

#  deleting an acount info(including password) from db.
    def del_pass(app):
        with conn:
            try:
                c.execute("DELETE FROM info WHERE appName=(?)", (app,))
                print('Your info for {0} has been deleted.'.format(app))
            except error:
                print('The vault does\'nt contain {0} acount info'.format(
                    app.title()))

# Entering the main password and checking if it's true/
    right = '12345'
    pas = input('Please enter your password to the VAULT: ')
    if pas == right:
        print('Your\'e in')
        while True:
            print('''
                ############################################
                ############################################
                ############################################
                 ''')
            print('''
                a --> Press a if you want to add a new password.
                g --> Press g if you want to get a specific password.
                u --> Press u if you want to update your info.
                d --> Press d if you want to delete a password.
                q --> Press q if you want to get out of the vault.
                ''')
            choice = input('What would you like to do: ')

            if choice.lower().strip() == 'a':

                app = input('App: ').lower()
                mail = input('Mail: ')
                dec = input('Would you like to get random password: ')

                if dec.lower() in ['yes', 'y']:
                    p = random_pass()
                    pyperclip.copy(p)
                    print('Random password has been copied to your clipboard.')
                else:
                    p = input('Enter password: ')

                if mail_check(mail) == True:
                    insert(app, mail, p)
                else:
                    print('Unvalid mail\nTry again!')
                    continue

            elif choice.lower().strip() == 'g':
                app = input('App: ').lower()

                get_pass(app)

            elif choice.lower().strip() == 'u':
                app = input('App: ')
                np = input('Enter your new password: ')

                update_pass(app, np)

            elif choice.lower().strip() == 'd':
                app = input('What app do you want to delete: ')
                del_pass(app)

            elif choice.lower().strip() == 'q':
                # Quiting the program and signing out.
                print('Good Bye...')
                break
                conn.close()
    else:
        print('WRONG PASSWORD!')
        conn.close()


main()
