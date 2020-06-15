from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import sqlite3


# CREATE AN SQLITE DATABASE

# acc_db = sqlite3.connect("accounts.db")
# c = acc_db.cursor()
# c.execute("""CREATE TABLE account(
#             name text,
#             email text,
#             password text)""")
# acc_db.commit()
# acc_db.close()


class MainScreen(Screen):
    main_email = ObjectProperty(None)
    main_pw = ObjectProperty(None)

    def submit(self):
        email = self.main_email.text.strip().lower()
        pw = self.main_pw.text.strip()
        with sqlite3.connect("accounts.db") as acc_db:
            cursor = acc_db.cursor()
            cursor.execute("SELECT email, password FROM account")
            accounts = cursor.fetchall()
            account = (email, pw)
            if account in accounts:
                self.clear()
                self.manager.current = "account"
            else:
                popup = Popup(title="Invalid Account",
                              content=Label(text="Please enter correct username/password"),
                              size_hint=(0.5, 0.25))
                popup.open()

    def clear(self):
        self.main_email.text = ""
        self.main_pw.text = ""


class RegisterScreen(Screen):
    r_name = ObjectProperty(None)
    r_email = ObjectProperty(None)
    r_pw = ObjectProperty(None)

    def submit(self):
        name = self.r_name.text.strip().lower()
        email = self.r_email.text.strip().lower()
        password = self.r_pw.text.strip()
        with sqlite3.connect("accounts.db") as acc_db:
            cursor = acc_db.cursor()
            cursor.execute("SELECT email FROM account")
            accounts = cursor.fetchall()
            if name == "" or email == "" or password == "" or "@" not in email:
                self.pop_up("invalid")
            elif email in str(accounts):
                print("duplicate found")
                self.pop_up("duplicate")
            else:
                cursor.execute("INSERT INTO account VALUES(:name, :email, :password)",
                               {"name": name,
                                "email": email,
                                "password": password})
                acc_db.commit()
                self.clear()
                self.manager.current = "main"

    def pop_up(self, error):
        if error == "invalid":
            win = Popup(title="Oops! Something went wrong",
                        content=Label(text="Have you entered the correct name, email and password?"),
                        size_hint=(0.5, 0.2))
            win.open()
        elif error == "duplicate":
            win = Popup(title="Oops! Something went wrong",
                        content=Label(text="Account already exists, please use a different email."),
                        size_hint=(0.5, 0.2))
            win.open()

    def clear(self):
        self.r_name.text = ""
        self.r_email.text = ""
        self.r_pw.text = ""


class AccountScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    def __init__(self):
        super(ScreenManagement, self).__init__()
        self.current = "main"


class LogSystem(App):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    LogSystem().run()
