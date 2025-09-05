import json
import os
import base64
from cryptography.fernet import Fernet
import secrets
import string
import random
import pyperclip
import tkinter as tk
from tkinter import messagebox,simpledialog

MASTER_PASSWORD="your_password"
DATA_FILE="data.json"
KEY_FILE="key.key"
def generate_key():
    if not os.path.exists(KEY_FILE):
        key=Fernet.generate_key()
        with open(KEY_FILE,"wb") as key_file:
            key_file.write(key)

def load_key():
    return open(KEY_FILE,"rb").read()
generate_key()
fernet=Fernet(load_key())
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE,"rb") as f:
        encrypted=f.read()
        if not encrypted:
            return {}
        decrypted=fernet.decrypt(encrypted)
        return json.loads(decrypted)
def save_data(data):
    encrypted=fernet.encrypt(json.dumps(data).encode())
    with open(DATA_FILE,"wb") as f:
        f.write(encrypted)


def generate_password(length=12):
    if length<4:
        raise ValueError("password length must be atleast 4 characters")
    lowercase=string.ascii_lowercase
    uppercase=string.ascii_uppercase
    digits=string.digits
    special=string.punctuation
    password=[secrets.choice(lowercase),
              secrets.choice(uppercase),
              secrets.choice(digits),
              secrets.choice(special),]
    all_chars=lowercase+uppercase+digits+special
    password+=[secrets.choice(all_chars) for _ in range(length -4)]
    random.shuffle(password)
    return ''.join(password)


def add_password():
    site=site_entry.get()
    username=user_entry.get()
    password=pass_entry.get()
    if not site or not username or not password:
        messagebox.showerror("error ","All fields are required!")
        return
    
    data=load_data()
    data[site]={"username":username,"password":password}
    save_data(data)
    messagebox.showinfo("success ",f"password for {site} saved!")
    site_entry.delete(0,tk.END)
    user_entry.delete(0,tk.END)
    pass_entry.delete(0,tk.END)


def retrieve_password():
    site=site_entry.get()

    data=load_data()
    if site in data:
        username=data[site]["username"]
        password=data[site]["password"]
        pyperclip.copy(password)
        messagebox.showinfo("Retrieved",f"Username: {username}\nPassword copied")

    else:
        messagebox.showerror("error",f"No entry found for {site}")
def delete_password():
    site=site_entry.get()
    data=load_data()
    if site in data:
        del data[site]
        save_data(data)
        messagebox.showinfo("Deleted",f"entry for {site} deleted")
    else:
        messagebox.showerror("error",f"No entry found for {site}")
def generate_password_gui():
    password=generate_password()
    pass_entry.delete(0,tk.END)
    pass_entry.insert(0,password)
    pyperclip.copy(password)
    messagebox.showinfo("generated","strong password generated & copied to clipboard")
def search_sites(event=None):
    query=search_entry.get().lower()
    results_listbox.delete(0,tk.END)
    data=load_data()
    for site in data:
        if query in site.lower():
            results_listbox.insert(tk.END,site)
'''def main():
    master=input("enter master password: ")
    if master != MASTER_PASSWORD:
        print("Incorrect master password! Exiting...")
        return
    while True:
        print("\nOptions:add/retrieve/delete/generate/exit")
        choice=input("enter choice: ").lower()
        if choice=="add":
            add_password()
        elif choice=="retrieve":
            retrieve_password()
        elif choice=="delete":
            delete_password()
        elif choice=="generate":
            print("Generated strong  password: ",generate_password())
        elif choice=="exit":
            print("exiting password manager")
            break
        else:
            print("invalid choice!")
if __name__=="__main__":
    main()'''
root=tk.Tk()
root.withdraw()
master=simpledialog.askstring("login","Enter master Password:",show="*")
if master !=MASTER_PASSWORD:
    messagebox.showerror("error","Incorrect master password !")
    root.destroy()
    exit()
root.deiconify()
root.title("password Manager")
root.geometry("400x550")
tk.Label(root,text="Site/Service: ").pack()
site_entry=tk.Entry(root,width=30)
site_entry.pack()
tk.Label(root,text="Username/Email:").pack()
user_entry=tk.Entry(root,width=30)
user_entry.pack()
tk.Label(root,text="password: ").pack()
pass_entry=tk.Entry(root,width=30)
pass_entry.pack()
tk.Label(root,text="Search site:").pack()
search_entry=tk.Entry(root,width=30)
search_entry.pack()
results_listbox=tk.Listbox(root,width=50)
results_listbox.pack()
search_entry.bind("<KeyRelease>",search_sites)
tk.Button(root,text="Add Password",command=add_password).pack(pady=5)
tk.Button(root,text="Retrieve password",command=retrieve_password).pack(pady=5)
tk.Button(root,text="Delete Password",command=delete_password).pack(pady=5)
tk.Button(root,text="Generate strong password",command=generate_password_gui).pack(pady=5)

root.mainloop()
