import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, auth_manager, show_register, open_finance_gui):

        super().__init__(parent)

        self.auth_manager = auth_manager

        self.show_register = show_register

        self.open_finance_gui = open_finance_gui

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="Personal Finance Manager",
            font=("Arial", 30, "bold")
        )

        title.pack(
            pady=(40, 10)
        )

        welcome = ctk.CTkLabel(
            self,
            text="Welcome Back!",
            font=("Arial", 22)
        )

        welcome.pack(
            pady=(0, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Login to continue",
            font=("Arial", 14)
        )

        subtitle.pack(
            pady=(0, 25)
        )

        # =====================================
        # FORM
        # =====================================

        form = ctk.CTkFrame(self)

        form.pack(
            padx=30,
            pady=10
        )

        ctk.CTkLabel(
            form,
            text="Email"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.email_entry = ctk.CTkEntry(
            form,
            width=300,
            placeholder_text="Enter your email"
        )

        self.email_entry.grid(
            row=0,
            column=1,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            form,
            text="Password"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.password_entry = ctk.CTkEntry(
            form,
            width=300,
            show="*",
            placeholder_text="Enter your password"
        )

        self.password_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=15
        )

        # =====================================
        # BUTTONS
        # =====================================

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=20
        )

        self.login_button = ctk.CTkButton(
            button_frame,
            text="Login",
            width=150,
            command=self.login
        )

        self.login_button.pack(
            pady=10
        )

        self.register_button = ctk.CTkButton(
            button_frame,
            text="Create Account",
            width=150,
            fg_color="transparent",
            border_width=1,
            command=self.show_register
        )

        self.register_button.pack(
            pady=5
        )

    # =====================================
    # METHODS
    # =====================================

    def login(self):

        email = self.email_entry.get().strip()

        password = self.password_entry.get()

        user = self.auth_manager.login(
            email,
            password
        )

        if user:

            self.clear_form()

            self.open_finance_gui(user)

        else:

            CTkMessagebox(
                title="Login Failed",
                message="Invalid email or password.",
                icon="cancel"
            )

    # =====================================
    # CLEAR FORM
    # =====================================

    def clear_form(self):

        self.email_entry.delete(0, "end")

        self.password_entry.delete(0, "end")


