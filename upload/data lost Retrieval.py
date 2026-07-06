# import libraries
import os
import shutil
import sqlite3
import hashlib
from tkinter import *
from tkinter import filedialog,messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
# Database Setup
conn = sqlite3.connect("recovery_logs.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, action TEXT)""")
conn.commit()
#main window
root = Tk()
root.title("Lost Data Retrieval System")
root.geometry("700x600")
root.configure(bg="lightblue")
#Title
title = Label(root,text="Lost Data Retrieval System",font=("Arial",24, "bold"),bg="lightblue")
title.pack(pady=20)
#login Frame
login_frame = Frame(root,bg="lightblue")
login_frame.pack(pady=20)
username_label = Label(login_frame,text="username",bg="lightblue",font=("Arial",13))
username_label.grid(row=0,column=0,padx=10,pady=10)
username_entry = Entry(login_frame,width=30)
username_entry.grid(row=0,column=1)
password_label = Label(login_frame,text="password",bg="lightblue",font=("Arial",13))
password_label.grid(row=1,column=0,padx=10,pady=10)
password_entry = Entry(login_frame,width=30, show="*")
password_entry.grid(row=1,column=1)
#global variable
selected_folder = ""
#login Function
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "1234": messagebox.showinfo("Success","Login Successful")
    else:
        messagebox.showerror("Error","Invalid username or password")
#select folder
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        folder_label.config(text=selected_folder)
    else:
        messagebox.showerror("Error","No Folder Selected")
#file scanner
def scan_files():
    if selected_folder == "":
        messagebox.showerror("Error","Please Select Folder First")
        return
    file_list.delete(0,END)
    try:
        files = os.listdir(selected_folder)
        if len(files) ==0:
            messagebox.showinfo("Info","Folder is empty")
            return
        for file in files:
            full_path = os.path.join(selected_folder, file)
            if os.path.isdir(full_path):
                file_list.insert(END, file)
    except Exception as e:
        messagebox.showerror("Error",str(e))

#backup function
def backup_files():
    if selected_folder == "":
        messagebox.showerror("Error","Please Select Folder")
        return
    backup_folder = "backup_files"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    files = os.listdir(selected_folder)
    for file in files:
        source = os.path.join(selected_folder, file)
        destination = os.path.join(backup_folder, file)
        if os.path.isfile(source):shutil.copy(source,destination)
        cursor.execute("INSERT INTO logs(filename, action)VALUES(?, ?)",(file, "backup Created"))
    conn.commit()
    messagebox.showinfo("Success","Backup Complete")
#recovery Function
def recover_files():
    backup_folder = "backup_files"
    recovered_folder = "recovered_files"
    if not os.path.exists(backup_folder):
        messagebox.showerror("Error","no backup found")
        return
    if not os.path.exists(recovered_folder):
        os.makedirs(recovered_folder)
    files = os.listdir(backup_folder)
    for file in files:
        source = os.path.join(backup_folder,file)
        destination = os.path.join(recovered_folder, file)
        if os.path.isfile(source):
            shutil.copy(source,destination)
    cursor.execute("INSERT INTO logs(filename, action) VALUES(?, ?)",(file, "File Recovered"))
    conn.commit()
    messagebox.showinfo("success","Recovery Completed")
#ecncrytion function
def encrypt_files():
    backup_folder = "backup_files"
    encrypted_folder = "encrypted_files"
    if not os.path.exists(backup_folder):
        messagebox.showerror("Error","no backup found")
        return
    if not os.path.exists(encrypted_folder):
        os.makedirs(encrypted_folder)
    files = os.listdir(backup_folder)
    for file in files:
        source = os.path.join(backup_folder, file)
        destination = os.path.join(encrypted_folder, file + ".enc")
        if os.path.isfile(source):
            shutil.copy(source,destination)
    messagebox.showinfo("success","Encryption Completed")

def show_logs():
    log_window = Toplevel(root)
    log_window.title("Recovery Logs")
    log_window.geometry("500x400")
    log_list = Listbox(log_window, width=70)
    log_list.pack(pady=20)
    cursor.execute("SELECT * FROM  logs")
    rows = cursor.fetchall()
    for row in rows:
        log_list.insert(END,f"ID: {row[0]} | File: {row[1]} | Action: {row[2]}")
#buttons
login_button = Button(root,text="Login",width=20,bg="green",fg="white",command=login)
login_button.pack(pady=10)
select_button = Button(root,text="Select Folder",width=20,command=select_folder)
select_button.pack(pady=10)
folder_label = Label(root,text="No Folder Selected",bg="lightblue",font=("Arial", 10))
folder_label.pack(pady=5)
scan_button = Button(root,text="Scan Files",width=20, command=scan_files)
scan_button.pack(pady=10)
backup_button = Button(root,text="Create Backup",width=20,command=backup_files)
backup_button.pack(pady= 10)
recover_button = Button(root,text="Recover Selected Files",width=20,command=recover_files)
recover_button.pack(pady=10)
encrypt_button = Button(root,text="encrypt selected file",width=20,command=encrypt_files)
encrypt_button.pack(pady=10)
logs_button = Button(root,text="Show Logs",width=20,command=show_logs)
logs_button.pack(pady=10)
#file list
file_list = Listbox(root, width=70,height=15)
file_list.pack(pady=20)
#run Application(
root.mainloop()
#close database
conn.close()