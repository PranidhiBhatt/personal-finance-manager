import customtkinter as ctk

from auth import AuthManager
from gui import FinanceGUI

from pages.login_page import LoginPage
from pages.register_page import RegisterPage

class LoginWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Personal Finance Manager")

        self.geometry("900x600")

        self.resizable(False, False)

        self.container = ctk.CTkFrame(self)

        self.container.pack(
            fill="both",
            expand=True
        )

        self.auth_manager = AuthManager()
        
        self.login_page = LoginPage(
            self.container,
            self.auth_manager,
            self.show_register,
            self.open_finance_gui
        )

        self.register_page = RegisterPage(
            self.container,
            self.auth_manager,
            self.show_login
        )

        self.login_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.register_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.show_login()

    def show_login(self):

        self.login_page.tkraise()


    def show_register(self):

        self.register_page.tkraise()

    def open_finance_gui(self, user):

        self.destroy()

        app = FinanceGUI(user)

        app.mainloop()
