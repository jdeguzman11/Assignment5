# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# a5.py

"""Main program for DS Messneger GUI."""

import tkinter as tk
from tkinter import ttk

from Profile import Profile


def main():
    root = tk.Tk()
    root.title("ICS 32 Distributed Social Messenger")
    root.geometry("700x500")

    profile = Profile()

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
    contacts_frame.rowconfigure(1, weight=0)
    contacts_frame.columnconfigure(0, weight=1)

    messages_frame.rowconfigure(0, weight=1)
    messages_frame.columnconfigure(0, weight=1)

    input_frame.rowconfigure(0, weight=1)
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=0)

    contacts_list = tk.Listbox(contacts_frame)
    contacts_list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    for contact in profile.contacts:
        contacts_list.insert(tk.END, contact)

    add_user_button = ttk.Button(contacts_frame, text="Add User")
    add_user_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    message_display = tk.Text(messages_frame, state="disabled", wrap="word")
    message_display.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    message_input = tk.Text(input_frame, height=4, wrap="word")
    message_input.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    send_button = ttk.Button(input_frame, text="Send Message")
    send_button.grid(row=0, column=1, sticky="se", padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
