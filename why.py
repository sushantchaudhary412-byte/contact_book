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

def add_contact():
    name = name_var.get().strip()
    phone = phone_var.get().strip()
    email = email_var.get().strip()

    if name and phone:
        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "favourite": False,
            "blocked": False
        }
        contacts.append(contact)
        contacts.sort(key=lambda x: x['name'].lower())
        save_contacts()
        refresh_table()
        clear_fields()
    else:
        messagebox.showwarning("Required", "Name and Phone are required.")

def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")

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

def edit_contact():
    selected = tree.selection()
    if selected:
        idx = tree.index(selected[0])
        contact = contacts[idx]

        new_name = simpledialog.askstring("Edit Name", "Name:", initialvalue=contact["name"])
        new_phone = simpledialog.askstring("Edit Phone", "Phone:", initialvalue=contact["phone"])
        new_email = simpledialog.askstring("Edit Email", "Email:", initialvalue=contact["email"])

        if new_name and new_phone:
            contacts[idx] = {
                "name": new_name,
                "phone": new_phone,
                "email": new_email or "",
                "favourite": contact.get("favourite", False),
                "blocked": contact.get("blocked", False)
            }
            contacts.sort(key=lambda x: x['name'].lower())
            save_contacts()
            refresh_table()
        else:
            messagebox.showwarning("Required", "Name and Phone can't be empty.")

def refresh_table(filtered=None):
    tree.delete(*tree.get_children())
    data = filtered if filtered is not None else contacts
    for contact in data:
        status = "⭐" if contact.get("favourite") else "🚫" if contact.get("blocked") else "Normal"
        tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"], status))

def search_contact(event=None):
    keyword = search_var.get().lower()
    tree.delete(*tree.get_children())
    for contact in contacts:
        if keyword in contact["name"].lower():
            status = "⭐" if contact.get("favourite") else "🚫" if contact.get("blocked") else "Normal"
            tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"], status))

def toggle_favourite():
    selected = tree.selection()
    if selected:
        idx = tree.index(selected[0])
        contacts[idx]["favourite"] = not contacts[idx].get("favourite", False)
        if contacts[idx]["favourite"]:
            contacts[idx]["blocked"] = False
        save_contacts()
        refresh_table()
    else:
        messagebox.showinfo("Select", "Select a contact to favourite/unfavourite.")

def toggle_blocked():
    selected = tree.selection()
    if selected:
        idx = tree.index(selected[0])
        contacts[idx]["blocked"] = not contacts[idx].get("blocked", False)
        if contacts[idx]["blocked"]:
            contacts[idx]["favourite"] = False
        save_contacts()
        refresh_table()
    else:
        messagebox.showinfo("Select", "Select a contact to block/unblock.")

def show_favourites():
    favs = [c for c in contacts if c.get("favourite")]
    if favs:
        refresh_table(filtered=favs)
    else:
        messagebox.showinfo("Favourites", "No favourite contacts yet.")

def show_blocked():
    blocked = [c for c in contacts if c.get("blocked")]
    if blocked:
        refresh_table(filtered=blocked)
    else:
        messagebox.showinfo("Blocked", "No blocked contacts yet.")

# ------------------- GUI MAIN WINDOW -------------------
def show_contact_book():
    global root, name_var, phone_var, email_var, search_var, tree, contacts

    root = tk.Tk()
    root.title("Contact Book")
    root.state("zoomed")
    root.resizable(False, False)

    # Menu Bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    main_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Menu", menu=main_menu)

    main_menu.add_command(label="⭐ Favourites", command=show_favourites)
    main_menu.add_command(label="🚫 Blocked Contacts", command=show_blocked)
    main_menu.add_command(label="🔄 Clear", command=lambda: refresh_table())
    main_menu.add_separator()
    main_menu.add_command(label="❌ Exit", command=root.quit)

    # Input Form
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

    # Search box
    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
    tk.Entry(search_frame, textvariable=search_var, width=30).pack(side=tk.LEFT)
    tk.Button(search_frame, text="🔍", command=search_contact, bg="black", fg="white").pack(side=tk.LEFT, padx=5)

    # Treeview
    table_frame = tk.Frame(root)
    table_frame.pack(pady=10, fill="both", expand=True)

    tree_scroll = tk.Scrollbar(table_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(table_frame, columns=("Name", "Phone", "Email", "Status"), show="headings", yscrollcommand=tree_scroll.set)
    tree.heading("Name", text="Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Email", text="Email")
    tree.heading("Status", text="Status")
    tree.column("Name", width=160, anchor="w")
    tree.column("Phone", width=120, anchor="center")
    tree.column("Email", width=180, anchor="w")
    tree.column("Status", width=80, anchor="center")
    tree.pack(fill="both", expand=True)

    tree_scroll.config(command=tree.yview)

    # Action Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Edit Contact", bg="#FFC107", fg="black", width=20, command=edit_contact).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Delete Selected", bg="#F44336", fg="white", width=20, command=delete_contact).grid(row=0, column=1, padx=10)

    tk.Button(btn_frame, text="⭐ Favourite", bg="#2196F3", fg="white", width=20, command=toggle_favourite).grid(row=1, column=0, pady=5)
    tk.Button(btn_frame, text="🚫 Block", bg="#9C27B0", fg="white", width=20, command=toggle_blocked).grid(row=1, column=1, pady=5)

    contacts = load_contacts()
    refresh_table()

    search_var.trace_add("write", lambda *args: search_contact())

    root.mainloop()

# ------------------- APP LOCK SCREEN -------------------
def show_app_lock():
    lock_window = tk.Tk()
    lock_window.title("App Lock")
    lock_window.geometry("300x300")
    lock_window.resizable(False, False)

    tk.Label(lock_window, text="Enter Password to Unlock").pack(pady=10)
    password_entry = tk.Entry(lock_window, show="*")
    password_entry.pack()

    def unlock():
        password = password_entry.get()
        if password == "1317":  # Change password here
            lock_window.destroy()
            show_contact_book()
        else:
            messagebox.showerror("Error", "Incorrect Password")

    tk.Button(lock_window, text="Unlock", command=unlock, bg="blue", fg="white").pack(pady=15)
    lock_window.mainloop()

# ------------------- Start App -------------------
show_app_lock()
