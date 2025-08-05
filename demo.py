import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json, os

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
        json.dump(contacts, f, indent=4)

# Add contact with auto alphabetical insertion
def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if name and phone:
        contact = {"name": name, "phone": phone, "email": email}
        contacts.append(contact)
        contacts.sort(key=lambda x: x['name'].lower())  # Alphabetical
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

# Delete selected contacts
def delete_contact():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showinfo("Select", "Select contact(s) to delete.")
        return

    for item in selected_items:
        idx = tree.index(item)
        contacts.pop(idx)
    save_contacts()
    refresh_table()

# Edit contact
def edit_contact():
    selected = tree.selection()
    if selected:
        idx = tree.index(selected[0])
        contact = contacts[idx]

        new_name = simpledialog.askstring("Edit Name", "Name:", initialvalue=contact["name"])
        new_phone = simpledialog.askstring("Edit Phone", "Phone:", initialvalue=contact["phone"])
        new_email = simpledialog.askstring("Edit Email", "Email:", initialvalue=contact["email"])

        if new_name and new_phone:
            contacts[idx] = {"name": new_name, "phone": new_phone, "email": new_email or ""}
            contacts.sort(key=lambda x: x['name'].lower())
            save_contacts()
            refresh_table()
        else:
            messagebox.showwarning("Required", "Name and Phone can't be empty.")

# Refresh table
def refresh_table():
    tree.delete(*tree.get_children())
    for contact in contacts:
        tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))

# Filter contacts
def search_contact(event=None):
    keyword = search_var.get().lower()
    tree.delete(*tree.get_children())
    for contact in contacts:
        if keyword in contact["name"].lower():
            tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))

# GUI setup
root = tk.Tk()
root.title("Contact Book")
root.geometry("600x550")
root.resizable(False, False)

# --- Input form ---
form_frame = tk.LabelFrame(root, text="Add New Contact", padx=10, pady=10)
form_frame.pack(pady=10, padx=10, fill="x")

name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()

tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w")
tk.Entry(form_frame, textvariable=name_var, width=25).grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky="w")
tk.Entry(form_frame, textvariable=phone_var, width=25).grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w")
tk.Entry(form_frame, textvariable=email_var, width=25).grid(row=2, column=1, padx=5)

tk.Button(form_frame, text="Add Contact", bg="#4CAF50", fg="white", width=20, command=add_contact).grid(row=3, columnspan=2, pady=10)

# --- Search box ---
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
tk.Entry(search_frame, textvariable=search_var, width=30).pack(side=tk.LEFT)
tk.Button(search_frame, text="🔍", command=search_contact, bg="black", fg="white").pack(side=tk.LEFT, padx=5)

# --- Treeview (Table) with Scrollbar ---
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True)

tree_scroll = tk.Scrollbar(table_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(table_frame, columns=("Name", "Phone", "Email"), show="headings", yscrollcommand=tree_scroll.set)
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.column("Name", width=180, anchor="w")
tree.column("Phone", width=130, anchor="center")
tree.column("Email", width=180, anchor="w")
tree.pack(fill="both", expand=True)

tree_scroll.config(command=tree.yview)

# --- Action buttons ---
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Edit Contact", bg="#FFC107", fg="black", width=20, command=edit_contact).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Delete Selected", bg="#F44336", fg="white", width=20, command=delete_contact).grid(row=0, column=1, padx=10)

# Load contacts and show
contacts = load_contacts()
refresh_table()

# Bind search on Enter key
search_var.trace_add("write", lambda *args: search_contact())

root.mainloop()
