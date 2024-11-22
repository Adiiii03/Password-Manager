from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for char in range(randint(8, 10))]
    password_symbol = [choice(symbols) for sym in range(randint(2, 4))]
    password_num = [choice(numbers) for num in range(randint(2, 4))]

    password_list = password_letter + password_symbol + password_num
    shuffle(password_list)

    password = "".join(password_list)
    pass_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    username = username_entry.get()
    password = pass_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {username}\nPassword: {password} \nIs it okay to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # reading old data
                    data = json.load(data_file)
                    # updating json file with new data
                    data.update(new_data)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                with open("data.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, "end")
                pass_entry.delete(0, "end")

# ---------------------------- SEARCH PASSWORD ------------------------------- #


def search_password():
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            content = json.load(data_file)
            if website in content:
                messagebox.showinfo(title=website, message=f"Email: {content[website]["email"]} \n"
                                                           f"Password: {content[website]["password"]}")

            else:
                messagebox.showinfo(message=f"No details for {website} exists.")

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#labels
website_label = Label(text="Website:", font=("Courier", 15))
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:", font=("Courier", 15))
username_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=("Courier", 15))
password_label.grid(column=0, row=3)

#Buttons
generate_button = Button(text="Generate Password", command=generate_pass)
generate_button.grid(column=2, row=3, )

add_button = Button(text="Add", width=34, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=13, command=search_password)
search_button.grid(column=2, row=1)

#Entries
website_entry = Entry(width=19)
website_entry.grid(column=1, row=1)

username_entry = Entry(width=36)
username_entry.insert(0, "adijustin9891@gmail.com")
username_entry.grid(column=1, row=2, columnspan=2)

pass_entry = Entry(width=19)
pass_entry.grid(column=1, row=3)


window.mainloop()
