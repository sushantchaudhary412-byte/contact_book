import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import json, os

# Global Variables
USER_FILE = "users.json"
contacts = []
current_user = None
contacts_file = None

# --------- Contact Functions ---------
def load_contacts():
    if os.path.exists(contacts_file):
        with open(contacts_file, "r") as f:
            try:
                raw_contacts = json.load(f)
                return [
                    {
                        "name": c["name"],
                        "phone": c["phone"],
                        "email": c.get("email", ""),
                        "status": c.get("status", "normal")
                    }
                    for c in raw_contacts
                ]
            except json.JSONDecodeError:
                return []
    return []

def save_contacts():
    with open(contacts_file, "w") as f:
        json.dump(contacts, f, indent=4)

# --------- User Functions ---------
def save_user(username, password):
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    if username in users:
        messagebox.showerror("Error", "Username already exists!")
        return
    users[username] = password
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def check_user(username, password):
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    return users.get(username) == password

# --------- Contact Management ---------
def add_contact():
    name, phone, email = name_var.get(), phone_var.get(), email_var.get()
    if not name or not phone:
        messagebox.showerror("Error", "Name and Phone are required!")
        return
    for c in contacts:
        if c["phone"] == phone:
            messagebox.showerror("Error", "Contact already exists!")
            return
    contacts.append({"name": name, "phone": phone, "email": email, "status": "normal"})
    save_contacts()
    refresh_table()
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    messagebox.showinfo("Success", "Contact added!")

def delete_contact():
    selected = tree.selection()
    for item in selected:
        values = tree.item(item, "values")
        contacts[:] = [c for c in contacts if not (c["name"] == values[0] and c["phone"] == values[1])]
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
            name = simpledialog.askstring("Edit", "New name:", initialvalue=c["name"])
            phone = simpledialog.askstring("Edit", "New phone:", initialvalue=c["phone"])
            email = simpledialog.askstring("Edit", "New email:", initialvalue=c["email"])
            if name and phone:
                contacts[i] = {"name": name, "phone": phone, "email": email, "status": c["status"]}
                break
    save_contacts()
    refresh_table()

def toggle_status(status_type):
    selected = tree.selection()
    for item in selected:
        values = tree.item(item, "values")
        for c in contacts:
            if c["name"] == values[0] and c["phone"] == values[1]:
                c["status"] = status_type if c["status"] != status_type else "normal"
                break
    save_contacts()
    refresh_table()

def show_filtered_contacts(status_type):
    filtered = [c for c in contacts if c["status"] == status_type]
    refresh_table(filtered)

def refresh_table(filtered=None):
    tree.delete(*tree.get_children())
    for c in (filtered if filtered is not None else contacts):
        tree.insert("", "end", values=(c["name"], c["phone"], c["email"], c["status"]))

def search_contact(*args):
    term = search_var.get().lower()
    filtered = [c for c in contacts if term in c["name"].lower() or term in c["phone"]]
    refresh_table(filtered)

# --------- Contact Book UI ---------
def show_contact_book():
    global name_var, phone_var, email_var, search_var, tree
    global input_frame, table_frame, btn_frame, search_frame, welcome_frame

    root = ctk.CTk()
    root.title("Contact Book")
    root.state("zoomed")
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Menubar
    menu = tk.Menu(root)
    root.config(menu=menu)
    main_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Menu", menu=main_menu)
    main_menu.add_command(label="➕ Add Contact", command=lambda: show_only("add"))
    main_menu.add_command(label="👁 Show Contacts", command=lambda: show_only("show"))
    main_menu.add_separator()
    main_menu.add_command(label="⭐ Favourites", command=lambda: show_filtered_contacts("favourite"))
    main_menu.add_command(label="🚫 Blocked", command=lambda: show_filtered_contacts("blocked"))
    main_menu.add_command(label="🔄 Show All", command=refresh_table)
    main_menu.add_separator()
    main_menu.add_command(label="❌ Exit", command=root.quit)

    # Variables
    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    search_var = tk.StringVar()

    # Welcome Frame
    welcome_frame = ctk.CTkFrame(root)
    welcome_frame.pack(pady=20)
    try:
        img = Image.open("contactbook_image.png").resize((600, 600))
        img_label = ctk.CTkLabel(welcome_frame, text="", image=ImageTk.PhotoImage(img))
        img_label.pack()
    except:
        ctk.CTkLabel(welcome_frame, text="Welcome to Contact Book").pack()

    # Input Frame
    input_frame = ctk.CTkFrame(root)
    ctk.CTkLabel(input_frame, text="Name").grid(row=0, column=0)
    ctk.CTkEntry(input_frame, textvariable=name_var).grid(row=0, column=1)
    ctk.CTkLabel(input_frame, text="Phone").grid(row=1, column=0)
    ctk.CTkEntry(input_frame, textvariable=phone_var).grid(row=1, column=1)
    ctk.CTkLabel(input_frame, text="Email").grid(row=2, column=0)
    ctk.CTkEntry(input_frame, textvariable=email_var).grid(row=2, column=1)
    ctk.CTkButton(input_frame, text="Add Contact", command=add_contact).grid(row=3, columnspan=2, pady=10)

    # Search Frame
    search_frame = ctk.CTkFrame(root)
    ctk.CTkLabel(search_frame, text="Search").pack(side="left", padx=5)
    ctk.CTkEntry(search_frame, textvariable=search_var, width=250).pack(side="left")
    ctk.CTkButton(search_frame, text="🔍", command=search_contact).pack(side="left", padx=5)

    # Table Frame
    table_frame = ctk.CTkFrame(root)
    scrollbar = tk.Scrollbar(table_frame)
    scrollbar.pack(side="right", fill="y")
    tree = ttk.Treeview(table_frame, columns=("Name", "Phone", "Email", "Status"), show="headings", yscrollcommand=scrollbar.set)
    for col in ("Name", "Phone", "Email", "Status"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    # Button Frame
    btn_frame = ctk.CTkFrame(root)
    ctk.CTkButton(btn_frame, text="Edit", command=edit_contact).grid(row=0, column=0, padx=10)
    ctk.CTkButton(btn_frame, text="Delete", command=delete_contact).grid(row=0, column=1, padx=10)
    ctk.CTkButton(btn_frame, text="⭐ Favourite", command=lambda: toggle_status("favourite")).grid(row=1, column=0)
    ctk.CTkButton(btn_frame, text="🚫 Block", command=lambda: toggle_status("blocked")).grid(row=1, column=1)

    def show_only(option):
        welcome_frame.pack_forget()
        input_frame.pack_forget()
        search_frame.pack_forget()
        table_frame.pack_forget()
        btn_frame.pack_forget()
        if option == "welcome":
            welcome_frame.pack(pady=20)
        elif option == "add":
            input_frame.pack(pady=10, fill="x", padx=20)
        elif option == "show":
            search_frame.pack(pady=5)
            table_frame.pack(pady=5, fill="both", expand=True)
            btn_frame.pack(pady=5)

    # Init data
    contacts.clear()
    contacts.extend(load_contacts())
    refresh_table()
    search_var.trace_add("write", search_contact)
    show_only("welcome")
    root.mainloop()

# --------- App Entry + Login ---------
def login_screen():
    def login():
        u, p = username.get(), password.get()
        if check_user(u, p):
            login_win.destroy()
            global current_user, contacts_file
            current_user = u
            contacts_file = f"{u}.json"
            unlock_app()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def signup():
        u, p = username.get(), password.get()
        if u and p:
            save_user(u, p)
            messagebox.showinfo("Success", "Account created.")
        else:
            messagebox.showerror("Error", "All fields required.")

    login_win = ctk.CTk()
    login_win.title("Login")
    login_win.geometry("400x500")
    frame = ctk.CTkFrame(login_win)
    frame.pack(pady=20)

    try:
        img = Image.open("contactbook_image.png").resize((250, 250))
        img_label = ctk.CTkLabel(frame, image=ImageTk.PhotoImage(img), text="")
        img_label.pack()
    except:
        ctk.CTkLabel(frame, text="Login to Contact Book").pack()

    username = tk.StringVar()
    password = tk.StringVar()
    ctk.CTkLabel(frame, text="Username").pack()
    ctk.CTkEntry(frame, textvariable=username).pack()
    ctk.CTkLabel(frame, text="Password").pack()
    ctk.CTkEntry(frame, textvariable=password, show="*").pack()

    ctk.CTkButton(frame, text="Login", command=login).pack(pady=10)
    ctk.CTkButton(frame, text="Sign Up", command=signup).pack()

    login_win.mainloop()

# --------- Unlock Screen ---------
def unlock_app():
    def check_password():
        if pwd_entry.get() == "1317":
            pwd_win.destroy()
            show_contact_book()
        else:
            messagebox.showerror("Error", "Wrong password!")

    pwd_win = ctk.CTk()
    pwd_win.title("Unlock App")
    pwd_win.geometry("300x150")

    ctk.CTkLabel(pwd_win, text="Enter Password").pack(pady=10)
    pwd_entry = ctk.CTkEntry(pwd_win, show="*")
    pwd_entry.pack(pady=5)
    ctk.CTkButton(pwd_win, text="Unlock", command=check_password).pack(pady=10)

    pwd_win.mainloop()

# Start App
login_screen()
