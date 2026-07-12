import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from account import AccountManager

class AccountPage(ctk.CTkFrame):

    def __init__(self, parent, account_manager, user):

        super().__init__(parent)

        self.user = user

        self.account_manager = account_manager

        # ==========================================
        # TITLE
        # ==========================================

        title = ctk.CTkLabel(
            self,
            text="Account Settings",
            font=("Arial", 28, "bold")
        )

        title.pack(
            pady=(20, 25)
        )

        main_frame = ctk.CTkFrame(self)

        main_frame.pack(
            padx=30,
            pady=20
        )

        ctk.CTkLabel(
            main_frame,
            text="Name"
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.name_entry = ctk.CTkEntry(
            main_frame,
            width=350
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            main_frame,
            text="Email"
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.email_entry = ctk.CTkEntry(
            main_frame,
            width=350
        )

        self.email_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=15
        )

        self.update_button = ctk.CTkButton(
            self,
            text="Update Profile",
            width=180,
            command=self.update_profile
        )

        self.update_button.pack(
            pady=20
        )

        self.load_profile()

    # ==========================================
    # LOAD PROFILE
    # ==========================================

    def load_profile(self):

        profile = self.account_manager.load_profile()

        if profile:

            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, profile[0])

            self.email_entry.delete(0, "end")
            self.email_entry.insert(0, profile[1])


    # ==========================================
    # UPDATE PROFILE
    # ==========================================

    def update_profile(self):

        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()

        success, message = self.account_manager.update_profile(
            name,
            email
        )

        if success:

            CTkMessagebox(
                title="Success",
                message=message,
                icon="check"
            )

        else:

            CTkMessagebox(
                title="Error",
                message=message,
                icon="cancel"
            )
