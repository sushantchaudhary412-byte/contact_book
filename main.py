import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json, os

# File path
FILE = "contacts.json"

# Load contacts
def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# Save contacts
def save_contacts():
    with open(FILE, "w") as f:
        json.dump(contacts, f)

# Add new contact
def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if name and phone:
        contact = {"name": name, "phone": phone, "email": email}
        contacts.append(contact)
        save_contacts()
        refresh_table()
        clear_fields()
    else:
        messagebox.showwarning("Required", "Name and Phone are required.")

# Clear input fields
def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")

# Delete contact
def delete_contact():
    selected = tree.selection()
    if selected:
        idx = tree.index(selected)
        contacts.pop(idx)
        save_contacts()
        refresh_table()
    else:
        messagebox.showinfo("Select", "Select a contact to delete.")

# Edit contact
def edit_contact():
    selected = tree.selection()
    if selected:
        idx = tree.index(selected)
        contact = contacts[idx]

        new_name = simpledialog.askstring("Edit Name", "Name:", initialvalue=contact["name"])
        new_phone = simpledialog.askstring("Edit Phone", "Phone:", initialvalue=contact["phone"])
        new_email = simpledialog.askstring("Edit Email", "Email:", initialvalue=contact["email"])

        if new_name and new_phone:
            contacts[idx] = {"name": new_name, "phone": new_phone, "email": new_email or ""}
            save_contacts()
            refresh_table()
        else:
            messagebox.showwarning("Required", "Name and Phone can't be empty.")

# Refresh table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for contact in contacts:
        tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))

# GUI
root = tk.Tk()
root.title("Contact Book")
root.geometry("500x500")
root.resizable(False, False)

# Input form
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()

tk.Label(form_frame, text="Name:").grid(row=0, column=0)
tk.Entry(form_frame, textvariable=name_var, width=25).grid(row=0, column=1)

tk.Label(form_frame, text="Phone:").grid(row=1, column=0)
tk.Entry(form_frame, textvariable=phone_var, width=25).grid(row=1, column=1)

tk.Label(form_frame, text="Email:").grid(row=2, column=0)
tk.Entry(form_frame, textvariable=email_var, width=25).grid(row=2, column=1)

tk.Button(form_frame, text="Add Contact", command=add_contact).grid(row=3, columnspan=2, pady=10)

# Treeview (Table)
tree = ttk.Treeview(root, columns=("Name", "Phone", "Email"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.pack(pady=10, fill=tk.X, padx=10)

# Action buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)
tk.Button(btn_frame, text="Edit", width=15, command=edit_contact).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete", width=15, command=delete_contact).grid(row=0, column=1, padx=5)

# Load and show
contacts = load_contacts()
refresh_table()

root.mainloop()