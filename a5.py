# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# a5.py

"""Main program for DS Messneger GUI."""

import tkinter as tk
from tkinter import ttk, simpledialog, filedialog

from Profile import Profile
from ds_messenger import DirectMessage, DirectMessenger


def main():
    root = tk.Tk()
    root.title("ICS 32 Distributed Social Messenger")
    root.geometry("700x500")

    profile = Profile()
    messenger = DirectMessenger(
        profile.dsuserver,
        profile.username,
        profile.password
        )

    def add_user():
        username = simpledialog.askstring("Add User", "Enter the Username:")
        if username:
            profile.add_contact(username)
            contacts_list.insert(tk.END, username)

    def load_profile():
        filepath = filedialog.askopenfilename(
            filetypes=[("DSU Files", "*.dsu")]
        )
        if not filepath:
            return

        profile.load_profile(filepath)

        contacts_list.delete(0, tk.END)
        for contact in profile.contacts:
            contacts_list.insert(tk.END, contact)

        message_display.config(state="normal")
        message_display.delete("1.0", tk.END)
        message_display.config(state="disabled")

    def show_conversation(event):
        selection = contacts_list.curselection()
        if not selection:
            return

        contact = contacts_list.get(selection[0])
        messages = profile.get_direct_messages(contact)

        message_display.config(state="normal")
        message_display.delete("1.0", tk.END)

        for msg in messages:
            message_display.insert(
                tk.END,
                f"{msg['recipient']}: {msg['message']}\n"
            )

        message_display.config(state="disabled")

    def send_message():
        selection = contacts_list.curselection()
        if not selection:
            return

        contact = contacts_list.get(selection[0])
        message_text = message_input.get("1.0", tk.END).strip()

        if not message_text:
            return

        sent = messenger.send(message_text, contact)
        print("Send result:", sent)

        new_message = DirectMessage(contact, message_text, "")
        profile.add_direct_message(contact, new_message)

        message_input.delete("1.0", tk.END)
        show_conversation(None)

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=4)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)

    contacts_frame = ttk.Frame(root, padding=5)
    contacts_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

    messages_frame = ttk.Frame(root, padding=5)
    messages_frame.grid(row=0, column=1, sticky="nsew")

    input_frame = ttk.Frame(root, padding=5)
    input_frame.grid(row=1, column=1, sticky="nsew")

    contacts_frame.rowconfigure(0, weight=1)
    contacts_frame.rowconfigure(2, weight=0)
    contacts_frame.columnconfigure(0, weight=1)

    messages_frame.rowconfigure(0, weight=1)
    messages_frame.columnconfigure(0, weight=1)

    input_frame.rowconfigure(0, weight=1)
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=0)

    contacts_list = tk.Listbox(contacts_frame)
    contacts_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    contacts_list.bind("<<ListboxSelect>>", show_conversation)

    for contact in profile.contacts:
        contacts_list.insert(tk.END, contact)

    add_user_button = ttk.Button(
        contacts_frame,
        text="Add User",
        command=add_user
        )
    add_user_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

    message_display = tk.Text(messages_frame, state="disabled", wrap="word")
    message_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    message_input = tk.Text(input_frame, height=4, wrap="word")
    message_input.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    send_button = ttk.Button(
        input_frame,
        text="Send Message",
        command=send_message
        )
    send_button.grid(row=0, column=1, sticky="se", padx=5, pady=5)

    load_profile_button = ttk.Button(
        contacts_frame,
        text="Load Profile",
        command=load_profile
    )
    load_profile_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
