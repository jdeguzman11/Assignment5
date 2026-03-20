# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# gui.py

"""GUI for DS Messenger."""

import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox

from Profile import Profile
from ds_messenger import DirectMessage, DirectMessenger


class MessengerGUI:
    """Main GUI application for DS Messenger."""

    def __init__(self, root):
        self.root = root
        self.root.title("ICS 32 Distributed Social Messenger")
        self.root.geometry("850x600")
        self.root.minsize(750, 500)

        self.profile = Profile()
        self.profile_path = None

        self.messenger = DirectMessenger(
            self.profile.dsuserver,
            self.profile.username,
            self.profile.password
        )

        self._configure_style()
        self._build_layout()
        self.root.after(5000, self.check_new_messages)

    def _configure_style(self):
        """Configure styling for interface."""
        self.root.configure(bg="#dbeafe")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Main.TFrame",
            background="#dbeafe"
        )

        style.configure(
            "Panel.TFrame",
            background="#bfdbfe",
            relief="flat"
        )

        style.configure(
            "Header.TLabel",
            background="#dbeafe",
            foreground="#1e3a8a",
            font=("Helvetica", 18, "bold")
        )

        style.configure(
            "Section.TLabel",
            background="#bfdbfe",
            foreground="#1e3a8a",
            font=("Helvetica", 11, "bold")
        )

        style.configure(
            "Info.TLabel",
            background="#dbeafe",
            foreground="#1f2937",
            font=("Helvetica", 10)
        )

        style.configure(
            "Primary.TButton",
            font=("Helvetica", 10, "bold"),
            padding=6
        )

        style.configure(
            "Secondary.TButton",
            font=("Helvetica", 10),
            padding=6
        )

    def _build_layout(self):
        """Create layout of GUI."""

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=0)
        self.root.rowconfigure(3, weight=0)

        header = ttk.Label(
            self.root,
            text="Distributed Social Messenger",
            style="Header.TLabel"
            )
        header.grid(
            row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(12, 8)
            )

        contacts_frame = ttk.Frame(self.root, padding=10, style="Panel.TFrame")
        contacts_frame.grid(
            row=1, column=0, rowspan=2, sticky="nsew", padx=(15, 8), pady=8
            )

        messages_frame = ttk.Frame(self.root, padding=10, style="Panel.TFrame")
        messages_frame.grid(
            row=1, column=1, sticky="nsew", padx=(15, 8), pady=8
            )

        input_frame = ttk.Frame(self.root, padding=10, style="Panel.TFrame")
        input_frame.grid(
            row=2, column=1, sticky="nsew", padx=(8, 15), pady=(6, 8)
            )

        status_frame = ttk.Frame(self.root, padding=8, style="Main.TFrame")
        status_frame.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=(0, 10)
        )

        contacts_frame.columnconfigure(0, weight=1)
        contacts_frame.rowconfigure(1, weight=1)

        messages_frame.columnconfigure(0, weight=1)
        messages_frame.rowconfigure(1, weight=1)

        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=0)

        ttk.Label(
            contacts_frame,
            text="Contacts",
            style="Section.TLabel"
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.contacts_list = tk.Listbox(
            contacts_frame,
            font=("Helvetica", 11),
            bg="white",
            fg="#111827",
            selectbackground="#60a5fa",
            selectforeground="white",
            activestyle="none",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#93c5fd"
        )
        self.contacts_list.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.contacts_list.bind("<<ListboxSelect>>", self.show_conversation)

        load_button = ttk.Button(
            contacts_frame,
            text="Load Profile",
            command=self.load_profile,
            style="Primary.TButton"
        )
        load_button.grid(row=2, column=0, sticky="ew", pady=(0, 6))

        add_button = ttk.Button(
            contacts_frame,
            text="Add User",
            command=self.add_user,
            style="Secondary.TButton"
        )
        add_button.grid(row=3, column=0, sticky="ew")

        ttk.Label(
            messages_frame,
            text="Conversation",
            style="Section.TLabel"
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.message_display = tk.Text(
            messages_frame,
            state="disabled",
            wrap="word",
            font=("Helvetica", 11),
            bg="white",
            fg="#111827",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#93c5fd",
            padx=8,
            pady=8
        )
        self.message_display.grid(row=1, column=0, sticky="nsew")

        ttk.Label(
            input_frame,
            text="Type your message",
            style="Section.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        self.message_input = tk.Text(
            input_frame,
            height=4,
            wrap="word",
            font=("Helvetica", 11),
            bg="white",
            fg="#111827",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#93c5fd",
            padx=8,
            pady=8
            )
        self.message_input.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self.message_input.bind("<Return>", self._send_with_enter)

        send_button = ttk.Button(
            input_frame,
            text="Send Message",
            command=self.send_message,
            style="Primary.TButton"
        )
        send_button.grid(row=1, column=1, sticky="se")

        self.status_label = ttk.Label(
            status_frame,
            text="Load a profile, select a contact, and type/send a message.",
            style="Info.TLabel"
        )
        self.status_label.grid(row=0, column=0, sticky="w")

    def _set_status(self, message: str):
        """Update status message at the bottom."""
        self.status_label.config(text=message)

    def _send_with_enter(self, event):
        """Send message with enter, newline = Shift+Enter."""
        if event.state & 0x0001:
            return
        self.send_message()
        return "break"

    def add_user(self):
        """Add new contact."""
        username = simpledialog.askstring("Add User", "Enter the Username:")

        if username:
            self.profile.add_contact(username)
            if username not in self.contacts_list.get(0, tk.END):
                self.contacts_list.insert(tk.END, username)
            self.save_profile()
            self._set_status(f"Added contact: {username}")

    def load_profile(self):
        """Load DSU profile."""
        filepath = filedialog.askopenfilename(
            filetypes=[("DSU Files", "*.dsu")]
        )

        if not filepath:
            return

        try:
            self.profile_path = filepath
            self.profile.load_profile(filepath)

            self.messenger.dsuserver = self.profile.dsuserver
            self.messenger.username = self.profile.username
            self.messenger.password = self.profile.password

            all_messages = self.messenger.retrieve_all()

            for msg in all_messages:
                contact = msg.recipient
                self.profile.add_contact(contact)
                self.profile.add_direct_message(contact, msg, "received")

            self.profile.remove_duplicate_messages()

            self.contacts_list.delete(0, tk.END)
            for contact in self.profile.contacts:
                self.contacts_list.insert(tk.END, contact)

            self.message_display.config(state="normal")
            self.message_display.delete("1.0", tk.END)
            self.message_display.config(state="disabled")

            self.save_profile()
            self._set_status("Profile loaded successfully.")
        except Exception as e:
            messagebox.showerror("Load Error", "Failed to load profile.")
            self._set_status("Failed to load profile.")

    def show_conversation(self, event=None):
        """Display messages for specific contact."""
        selection = self.contacts_list.curselection()

        if not selection:
            return

        contact = self.contacts_list.get(selection[0])
        messages = self.profile.get_direct_messages(contact)

        self.message_display.config(state="normal")
        self.message_display.delete("1.0", tk.END)

        for msg in messages:
            if msg["direction"] == "sent":
                self.message_display.insert(
                    tk.END,
                    f"You: {msg['message']}\n"
                )
            else:
                self.message_display.insert(
                    tk.END,
                    f"{contact}: {msg['message']}\n"
                )

        self.message_display.config(state="disabled")
        self._set_status(f"Viewing convo with {contact}.")

    def send_message(self):
        """Send message to specific contact."""
        selection = self.contacts_list.curselection()

        if not selection:
            messagebox.showinfo(
                "No Contact Selected",
                "Select a contact first."
                )
            self._set_status("Select a contact before sending.")
            return

        contact = self.contacts_list.get(selection[0])
        message_text = self.message_input.get("1.0", tk.END).strip()

        if not message_text:
            messagebox.showinfo(
                "Empty Message",
                "Please type a message before sending."
            )
            self._set_status("Message box is empty.")
            return

        sent = self.messenger.send(message_text, contact)

        if sent:
            new_message = DirectMessage(contact, message_text, "")
            self.profile.add_direct_message(contact, new_message, "sent")
            self.save_profile()

            self.message_input.delete("1.0", tk.END)
            self.show_conversation()
            self._set_status(f"Message sent to {contact}.")
        else:
            messagebox.showerror(
                "Send failed.",
                "Check your profile or server connection."
            )
            self._set_status("Send failed.")

    def check_new_messages(self):
        """Refresh for new messages."""
        if not (
            self.messenger.dsuserver
            and self.messenger.username
            and self.messenger.password
        ):
            self.root.after(5000, self.check_new_messages)
            return

        new_messages = self.messenger.retrieve_new()

        for msg in new_messages:
            contact = msg.recipient

            self.profile.add_contact(contact)
            self.profile.add_direct_message(contact, msg, "received")

            if contact not in self.contacts_list.get(0, tk.END):
                self.contacts_list.insert(tk.END, contact)

        if new_messages:
            self.profile.remove_duplicate_messages()
            self.save_profile()
            self.show_conversation()

        self.root.after(5000, self.check_new_messages)

    def save_profile(self):
        """Save profile if path exists."""
        if self.profile_path:
            self.profile.save_profile(self.profile_path)
