from tkinter import *
from tkinter import messagebox,simpledialog
import json
import random as random
import pyperclip
from cryptography.fernet import Fernet
# from Crypto.Cipher import AES
import base64,math


def nums_of_char():
    number_letters=simpledialog.askinteger(title="Amount of letters",prompt="Choose how many letters to use in password: ",parent=window,minvalue=4,maxvalue=12)
    number_numbers=simpledialog.askinteger(title="Amount of numbers",prompt="Choose how many numbers to use in password: ",parent=window,minvalue=4,maxvalue=12)
    number_symbols=simpledialog.askinteger(title="Amount of symbols",prompt="Choose how many symbols to use in password: ",parent=window,minvalue=4,maxvalue=12)
    return number_letters,number_numbers,number_symbols
def delete():
    '''this function deletes either a specific entry or all entries based on the optionmenu selected item'''
    website=website_entry.get()
    #input is checked in order to delete all entries or a specific one
    if var1.get()=="Delete aassigned entry":
        try:
            with open("login_data.json", "r") as file:
                data = json.load(file)
            data.pop(website)
            with open("login_data.json", "w") as file:
                json.dump(data, file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="There are no saved credentials")

        except json.decoder.JSONDecodeError:
            messagebox.showerror(title="Oops", message="Something went wrong")
    else:
        try:
            with open("login_data.json", "r") as file:
                data = json.load(file)
            data.clear()
            with open("login_data.json","w")as file:
                json.dump(data,file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="There are no saved credentials")

def view_all():
    '''View all credentials one by one'''
    try:
        with open("login_data.json","r") as file:
            data=json.load(file)
        #if data file is empty it outputs an appropriate message otherwise it loops through the data file and outputs all credentials
        if len(data)==0:
            messagebox.showerror(title="Oops",message="There are no saved credentials")
        else:
            for key in data.keys():
                messagebox.showinfo(title=f"{key.title()} credentials",message=f"Website: {key.title()}\nUsername: {data[key]['Username']}\nPassword: {data[key]['Password']}")
    except FileNotFoundError:
        messagebox.showerror(title="Error",message="No saved credentials found")
def search():
    '''Search a specific website from all saved credentials'''
    website=website_entry.get()
    if bool(website):
        try:
            with open("login_data.json") as file:
                data=json.load(file)

            if website in data:
                messagebox.showinfo(title=f"{website.title()} credentials",message=f"Username: {data[website]['Username']}\nPassword: {data[website]['Password']}")
            else:
                messagebox.showerror(title="Error",message="There are no credentials that match your search parameter")
        except FileNotFoundError:
            messagebox.showerror(title="Error",message="There are no saved credentials")
    else:
        messagebox.showerror(title="Oops",message="You haven't entered a website to search for")

def generate():
    '''letters numbers and symbols lists in order to generate random elements from each list to generate a password.Also copies password to clipboard
    You can either choose how many letters,numbers or symbols to use within a range of 4-12 or you can randomly generate the amount of characters'''
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_list=[]
    #if option menu 2's option is random amount of characters randomly generate the amount of characters to be created in the password
    if var2.get()=="Random amount of characters for generated password":
        num_let=random.randint(4,12)
        num_num=random.randint(4,12)
        num_sym=random.randint(4,12)
    else:
        #otherwise have 3 pop ups to define how many letters,numbers and symbols to have in the generated password
        num_let,num_num,num_sym=nums_of_char()
    for i in range(num_let):
        password_list.append(random.choice(letters))
    for i in range(num_num):
        password_list.append(random.choice(numbers))
    for i in range(num_sym):
        password_list.append(random.choice(symbols))
    #reorganizes the password list
    random.shuffle(password_list)
    #conver to string
    password_str="".join(password_list)
    #empty all entries and fill the password entry with the new password
    password_entry.delete(0,END)
    password_entry.insert(0,password_str)
    #copy password to clipboard
    pyperclip.copy(password_str)

def add():
    '''saves or updates credentials. if entries are vacant it outputs an appropriate message'''
    website=website_entry.get()
    username=username_entry.get()
    password=password_entry.get()
    new_data={website:{"Username":username,"Password":password}}
    if bool(website) and bool(password) and bool(username):
        try:
            with open("login_data.json","r") as file:
                data=json.load(file)
            #checks to see if there is already a password for the website. nif there is then the previous entry gets deleted and the new information is saved
            if website in data:
                del data[website]
                data.update(new_data)
            else:
                data.update(new_data)
            with open("login_data.json","w") as file:
                json.dump(data, file)
        except FileNotFoundError:
            with open("login_data.json","w") as file:
                json.dump(new_data,file)
        except json.decoder.JSONDecodeError:
            with open("login_data.json","w") as file:
                json.dump(new_data,file)
    else:
        messagebox.showerror(title="Error",message="You have not submitted all of the credentials")


window=Tk()
window.title("Password Manager")
window.config(padx=10,pady=10)

canvas=Canvas(width=200, height=200)
logo_img=PhotoImage(file="./logo.png")
image=canvas.create_image(100,100, image=logo_img)
canvas.grid(column=2,row=1)

website_label=Label(width=20, height=5, text="Website:")
website_label.grid(column=1,row=3)

website_entry=Entry(width=35)
website_entry.grid(column=2,row=3, columnspan=2)
website_entry.focus()

username_label=Label(width=20, height=5, text= "Email/Username:")
username_label.grid(column=1, row=4)

username_entry=Entry(width=35)
username_entry.insert(0,"giorgosadamidis@hotmail.com")
username_entry.grid(column=2,row=4, columnspan=2)
username=username_entry.get()


password_label=Label(width=20, height=5, text="Password:")
password_label.grid(column=1, row=5)


password_entry=Entry(width=21)
password_entry.grid(column=2, row=5)


generate_button=Button(text="Generate Password", command=generate)
generate_button.grid(column=4, row=4)

add_button=Button(text="Add", command=add, width=18, highlightthickness=0)
add_button.grid(column=4, row=7, columnspan=2)

view_all_button=Button(text="View All", command=view_all, width=18)
view_all_button.grid(column=4,row=5,columnspan=2)

search_button=Button(text="Search", command=search, width=18, highlightthickness=0)
search_button.grid(column=4, row=3)

delete_button=Button(text="Delete credentials",command=delete, width=18)
delete_button.grid(column=4,row=9)

var1=StringVar(window)
var1.set("Delete all entries")
op_menu=OptionMenu(window,var1,"Delete all entries","Delete assigned entry")
op_menu.grid(column=1,row=9)


var2=StringVar(window)
var2.set("Random amount of characters for generated password")
op_menu2=OptionMenu(window,var2,"Random amount of characters for generated password", "Assign number of characters")
op_menu2.grid(column=2,row=10)


window.mainloop()