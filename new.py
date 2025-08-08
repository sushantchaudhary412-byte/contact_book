import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import json, os

USER_FILE = "users.json"
contacts = []
current_user = None
contacts_file = None

# --------- Contact Book Functions ---------
def load_contacts():
    global contacts_file
    if os.path.exists(contacts_file):
        with open(contacts_file, "r") as f:
            raw_contacts = json.load(f)
            fixed_contacts = []
            for c in raw_contacts:
                status = c.get("status", "normal")
                if c.get("favourite"):
                    status = "favourite"
                if c.get("blocked"):
                    status = "blocked"
                fixed_contacts.append({
                    "name": c["name"],
                    "phone": c["phone"],
                    "email": c.get("email", ""),
                    "status": status
                })
            return fixed_contacts
    return []

def save_contacts():
    global contacts_file
    with open(contacts_file, "w") as f:
        json.dump(contacts, f, indent=4)

# --------- User Login/Signup Functions ---------
def save_user(username, password):
    users = {}
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    try:
        with open(USER_FILE, "r") as f:
            users = json.load(f)
    except json.JSONDecodeError:
        users = {}
    if username in users:
        messagebox.showerror("Error", "Username already exists!")
        return
    users[username] = password
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def check_user(username, password):
    if not os.path.exists(USER_FILE):
        return False
    try:
        with open(USER_FILE, "r") as f:
            users = json.load(f)
        return users.get(username) == password
    except json.JSONDecodeError:
        return False

# --------- Contact Management Functions ---------
def add_contact():
    name, phone, email = name_var.get(), phone_var.get(), email_var.get()
    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone are required!")
        return
    for c in contacts:
        if c["phone"] == phone:
            messagebox.showerror("Error", "Contact already exists!")
            return
    contact = {"name": name, "phone": phone, "email": email, "status": "normal"}
    contacts.append(contact)
    save_contacts()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Contact added!")

def delete_contact():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        values = tree.item(item, "values")
        for c in contacts:
            if c["name"] == values[0] and c["phone"] == values[1]:
                contacts.remove(c)
                break
    save_contacts()
    refresh_table()

def edit_contact():
    selected = tree.selection()
    if not selected:
        return
    item = selected[0]
    values = tree.item(item, "values")
    for i, c in enumerate(contacts):
        if c["name"] == values[0] and c["phone"] == values[1]:
            name = simpledialog.askstring("Edit", "Enter new name:", initialvalue=c["name"])
            phone = simpledialog.askstring("Edit", "Enter new phone:", initialvalue=c["phone"])
            email = simpledialog.askstring("Edit", "Enter new email:", initialvalue=c["email"])
            if name and phone:
                contacts[i] = {"name": name, "phone": phone, "email": email, "status": c["status"]}
                break
    save_contacts()
    refresh_table()

def refresh_table(filtered=None):
    tree.delete(*tree.get_children())
    data = filtered if filtered is not None else contacts
    for contact in data:
        status_text = contact["status"]
        emoji = "🙂"
        if status_text == "favourite":
            emoji = "⭐"
        elif status_text == "blocked":
            emoji = "🚫"
        display_status = f"{emoji} {status_text.capitalize()}"
        tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"], display_status))

def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")

def search_contact():
    term = search_var.get().lower()
    filtered = [c for c in contacts if term in c["name"].lower() or term in c["phone"]]
    refresh_table(filtered)

def toggle_favourite():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        values = tree.item(item, "values")
        for c in contacts:
            if c["name"] == values[0] and c["phone"] == values[1]:
                c["status"] = "favourite" if c["status"] != "favourite" else "normal"
                break
    save_contacts()
    refresh_table()

def toggle_blocked():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        values = tree.item(item, "values")
        for c in contacts:
            if c["name"] == values[0] and c["phone"] == values[1]:
                c["status"] = "blocked" if c["status"] != "blocked" else "normal"
                break
    save_contacts()
    refresh_table()

def show_favourites():
    filtered = [c for c in contacts if c["status"] == "favourite"]
    refresh_table(filtered)

def show_blocked():
    filtered = [c for c in contacts if c["status"] == "blocked"]
    refresh_table(filtered)

# --------- Main Contact Book UI ---------
def show_contact_book():
    global name_var, phone_var, email_var, search_var, tree
    global input_frame, table_frame, btn_frame, search_frame, welcome_frame

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Contact Book")
    root.state("zoomed")

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    main_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Menu", menu=main_menu)
    main_menu.add_command(label="➕ Add Contact", command=lambda: show_only("add"))
    main_menu.add_command(label="👁 Show Contacts", command=lambda: show_only("show"))
    main_menu.add_separator()
    main_menu.add_command(label="⭐ Favourites", command=show_favourites)
    main_menu.add_command(label="🚫 Blocked Contacts", command=show_blocked)
    main_menu.add_command(label="🔄 Show All", command=refresh_table)
    main_menu.add_separator()
    main_menu.add_command(label="❌ Exit", command=root.quit)

    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    search_var = tk.StringVar()

    welcome_frame = ctk.CTkFrame(root)
    welcome_frame.pack(pady=20)

    input_frame = ctk.CTkFrame(root)
    ctk.CTkLabel(input_frame, text="Name:").grid(row=0, column=0, sticky="w")
    ctk.CTkEntry(input_frame, textvariable=name_var).grid(row=0, column=1, padx=5)
    ctk.CTkLabel(input_frame, text="Phone:").grid(row=1, column=0, sticky="w")
    ctk.CTkEntry(input_frame, textvariable=phone_var).grid(row=1, column=1, padx=5)
    ctk.CTkLabel(input_frame, text="Email:").grid(row=2, column=0, sticky="w")
    ctk.CTkEntry(input_frame, textvariable=email_var).grid(row=2, column=1, padx=5)
    ctk.CTkButton(input_frame, text="Add Contact", command=add_contact).grid(row=3, columnspan=2, pady=10)

    search_frame = ctk.CTkFrame(root)
    ctk.CTkLabel(search_frame, text="Search:").pack(side="left", padx=5)
    ctk.CTkEntry(search_frame, textvariable=search_var, width=250).pack(side="left")
    ctk.CTkButton(search_frame, text="🔍", command=search_contact).pack(side="left", padx=5)

    table_frame = ctk.CTkFrame(root)
    tree_scroll = tk.Scrollbar(table_frame)
    tree_scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(table_frame, columns=("Name", "Phone", "Email", "Status"), show="headings", yscrollcommand=tree_scroll.set)
    for col in ("Name", "Phone", "Email", "Status"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True)
    tree_scroll.config(command=tree.yview)

    btn_frame = ctk.CTkFrame(root)
    ctk.CTkButton(btn_frame, text="Edit Contact", command=edit_contact, width=140).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btn_frame, text="Delete Selected", command=delete_contact, width=140).grid(row=0, column=1, padx=10)
    ctk.CTkButton(btn_frame, text="⭐ Favourite", command=toggle_favourite, width=140).grid(row=1, column=0, pady=5)
    ctk.CTkButton(btn_frame, text="🚫 Block", command=toggle_blocked, width=140).grid(row=1, column=1, pady=5)

    def show_only(option):
        welcome_frame.pack_forget()
        input_frame.pack_forget()
        search_frame.pack_forget()
        table_frame.pack_forget()
        btn_frame.pack_forget()

        if option == "welcome":
            welcome_frame.pack(pady=20)
        elif option == "add":
            input_frame.pack(pady=10, padx=10, fill="x")
        elif option == "show":
            search_frame.pack(pady=5)
            table_frame.pack(pady=10, fill="both", expand=True)
            btn_frame.pack(pady=10)
            refresh_table()

    contacts.clear()
    contacts.extend(load_contacts())
    refresh_table()
    search_var.trace_add("write", lambda *args: search_contact())

    show_only("welcome")
    root.mainloop()

# --------- Login Screen ---------
def login_screen():
    def login():
        u = username.get()
        p = password.get()
        if check_user(u, p):
            login_win.destroy()
            global current_user, contacts_file
            current_user = u
            contacts_file = f"{u}.json"
            show_contact_book()
        else:
            messagebox.showerror("Error", "Invalid login!")

    def signup():
        u = username.get()
        p = password.get()
        if u and p:
            save_user(u, p)
            messagebox.showinfo("Success", "Account created. Now log in.")
        else:
            messagebox.showerror("Error", "Username and Password required.")

    login_win = ctk.CTk()
    login_win.title("Login")
    login_win.geometry("400x600")

    frame = ctk.CTkFrame(login_win)
    frame.pack(pady=20)

    username = tk.StringVar()
    password = tk.StringVar()

    ctk.CTkLabel(frame, text="Username").pack(pady=5)
    ctk.CTkEntry(frame, textvariable=username).pack()
    ctk.CTkLabel(frame, text="Password").pack(pady=5)
    ctk.CTkEntry(frame, textvariable=password, show="*").pack()
    ctk.CTkButton(frame, text="Login", command=login).pack(pady=10)
    ctk.CTkButton(frame, text="Sign Up", command=signup).pack()

    login_win.mainloop()

# --------- App Unlock Password ---------
def unlock_app():
    def check_password():
        if pwd_entry.get() == "1317":
            pwd_win.destroy()
            login_screen()
        else:
            messagebox.showerror("Error", "Wrong password!")

    pwd_win = ctk.CTk()
    pwd_win.title("Enter Password")
    pwd_win.geometry("300x150")

    ctk.CTkLabel(pwd_win, text="Enter App Password:").pack(pady=10)
    pwd_entry = ctk.CTkEntry(pwd_win, show="*")
    pwd_entry.pack(pady=5)
    ctk.CTkButton(pwd_win, text="Unlock", command=check_password).pack(pady=10)

    pwd_win.mainloop()

# --------- Launch App ---------
unlock_app()
