# Justin DeGuzman
# justicd1@uci.edu
# 72329664

# a5.py

"""Main program for DS Messneger GUI."""

import tkinter as tk
from gui import MessengerGUI


def main():
    """Laucnh DS messenger GUI."""
    root = tk.Tk()
    MessengerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
