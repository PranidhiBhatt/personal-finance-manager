import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class RegisterPage(ctk.CTkFrame):

    def __init__(self, parent, auth_manager, show_login):

        super().__init__(parent)

        self.auth_manager = auth_manager

        self.show_login = show_login

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="Create Account",
            font=("Arial", 30, "bold")
        )

        title.pack(
            pady=(40, 10)
        )

        # =====================================
        # TITLE
        # =====================================

        title = ctk.CTkLabel(
            self,
            text="Create Account",
            font=("Arial", 30, "bold")
        )

        title.pack(
            pady=(40, 10)
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
            text="Full Name"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.name_entry = ctk.CTkEntry(
            form,
            width=300,
            placeholder_text="Enter your full name"
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            form,
            text="Email"
        ).grid(
            row=1,
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
            row=1,
            column=1,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            form,
            text="Password"
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.password_entry = ctk.CTkEntry(
            form,
            width=300,
            show="*",
            placeholder_text="Create a password"
        )

        self.password_entry.grid(
            row=2,
            column=1,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            form,
            text="Confirm Password"
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.confirm_password_entry = ctk.CTkEntry(
            form,
            width=300,
            show="*",
            placeholder_text="Confirm your password"
        )

        self.confirm_password_entry.grid(
            row=3,
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

        self.register_button = ctk.CTkButton(
            button_frame,
            text="Register",
            width=150,
            command=self.register
        )

        self.register_button.pack(
            pady=10
        )

        self.login_button = ctk.CTkButton(
            button_frame,
            text="Back to Login",
            width=150,
            fg_color="transparent",
            border_width=1,
            command=self.show_login
        )

        self.login_button.pack(
            pady=5
        )

    # =====================================
    # METHODS
    # =====================================

    def register(self):

        name = self.name_entry.get().strip()

        email = self.email_entry.get().strip()

        password = self.password_entry.get()

        confirm_password = self.confirm_password_entry.get()

        success, message = self.auth_manager.register(
            name,
            email,
            password,
            confirm_password
        )

        if success:

            CTkMessagebox(
                title="Success",
                message=message,
                icon="check"
            )

            self.clear_form()

            self.show_login()

        else:

            CTkMessagebox(
                title="Error",
                message=message,
                icon="cancel"
            )

    # =====================================
    # CLEAR FORM
    # =====================================

    def clear_form(self):

        self.name_entry.delete(0, "end")

        self.email_entry.delete(0, "end")

        self.password_entry.delete(0, "end")

        self.confirm_password_entry.delete(0, "end")


