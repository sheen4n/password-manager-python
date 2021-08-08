from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

EMAIL = "sheen.an.goh@gmail.com"
FILE = "passwords.json"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = [*letters_list, *symbols_list, *numbers_list]

    shuffle(password_list)
    password = ''.join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(
            title="Oops", message="Please don't leave any fields empty!")
        return

    new_password = {
        website: {
            "email": email,
            "password": password
        }
    }
    try:
        with open(FILE, "r") as password_file:
            data = json.load(password_file)
    except FileNotFoundError:
        with open(FILE, "w") as password_file:
            json.dump(new_password, password_file, indent=4)
    else:
        data.update(new_password)
        with open(FILE, "w") as password_file:
            json.dump(data, password_file, indent=4)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        messagebox.showinfo(
            title="Success", message="You have successfully saved the password!")


def get_password():
    website = website_entry.get()
    try:
        with open(FILE, "r") as password_file:
            existing_passwords = json.load(password_file)
            data = existing_passwords[website]

            password_entry.delete(0, END)
            password_entry.insert(0, data['password'])
            email_entry.delete(0, END)
            email_entry.insert(0, data['email'])
    except (FileNotFoundError, KeyError):
        messagebox.showinfo(
            title="Error", message="No passwords found!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=20)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=39)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, EMAIL)
password_entry = Entry(width=20)
password_entry.grid(row=3, column=1)

# Buttons
generate_password_button = Button(
    text="Generate Password", command=generate_password, width=16)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=39, command=save)
add_button.grid(row=4, column=1, columnspan=2)
fetch_password_button = Button(text="Search", command=get_password, width=16)
fetch_password_button.grid(row=1, column=2, columnspan=1)


window.mainloop()
