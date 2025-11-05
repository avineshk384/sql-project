import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

# ---------- BACKEND SETUP --------------
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="3804"
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS LoginDemo")
    cur.execute("USE LoginDemo")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )
    """)
    cur.execute("INSERT IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    cur.close()
    conn.close()
init_db()


# ---------- DASHBOARD AFTER LOGIN ------------
def show_dashboard(loggedin_user):
    dash = tk.Toplevel(root)
    dash.title("SQL User Dashboard")
    dash.geometry("475x420")
    dash.configure(bg="#f3f8fa")

    tk.Label(dash, text="User Database", font=("Arial Bold", 17), fg="#138d75", bg="#f3f8fa").pack(pady=12)

    tree = ttk.Treeview(dash, columns=("ID", "Username", "Password"), show="headings", height=7)
    tree.heading("ID", text="ID")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    for col in ("ID","Username","Password"): tree.column(col, width=115)
    tree.pack(padx=18, pady=6)

    def refresh_table():
        for row in tree.get_children(): tree.delete(row)
        conn = mysql.connector.connect(host="localhost", user="root", password="10382", database="LoginDemo")
        cur = conn.cursor()
        cur.execute("SELECT id, username, password FROM users")
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
        cur.close(); conn.close()
    refresh_table()

    # Add User Form
    add_frame = tk.Frame(dash, bg="#f3f8fa")
    tk.Label(add_frame, text="New Username:", font=("Arial", 10), bg="#f3f8fa").grid(row=0,column=0,padx=6,pady=4)
    enu = tk.Entry(add_frame, width=15)
    enu.grid(row=0,column=1)
    tk.Label(add_frame, text="New Password:", font=("Arial", 10), bg="#f3f8fa").grid(row=0,column=2,padx=6)
    epw = tk.Entry(add_frame, width=15)
    epw.grid(row=0,column=3)
    add_frame.pack(pady=3)

    def add_user():
        u = enu.get()
        p = epw.get()
        if not u or not p:
            messagebox.showwarning("Input", "Both fields required.", parent=dash)
            return
        conn = mysql.connector.connect(host="localhost", user="root", password="10382", database="LoginDemo")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users(username,password) VALUES(%s,%s)", (u,p))
            conn.commit()
            messagebox.showinfo("User Added", "User created successfully.", parent=dash)
            refresh_table()
        except:
            messagebox.showerror("Error", "Username already exists!", parent=dash)
        cur.close(); conn.close()
    tk.Button(add_frame, text="Add User", font=("Arial", 10), command=add_user, bg="#aed6f1", relief="ridge").grid(row=0,column=4,padx=8)

    # Delete User form
    del_frame = tk.Frame(dash, bg="#f3f8fa")
    tk.Label(del_frame, text="User ID to Delete:", font=("Arial", 10), bg="#f3f8fa").grid(row=0,column=0,padx=6,pady=5)
    eid = tk.Entry(del_frame, width=8)
    eid.grid(row=0,column=1)
    def delete_user():
        idv = eid.get()
        if not idv:
            messagebox.showwarning("Input", "Enter User ID.", parent=dash)
            return
        conn = mysql.connector.connect(host="localhost", user="root", password="10382", database="LoginDemo")
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id=%s",(idv,))
        if cur.rowcount>0:
            messagebox.showinfo("Deleted", "User deleted.", parent=dash)
        else:
            messagebox.showerror("Error", "No user with that ID.", parent=dash)
        conn.commit(); cur.close(); conn.close(); refresh_table()
    tk.Button(del_frame, text="Delete User", font=("Arial", 10), command=delete_user, bg="#f7c8c8", relief="ridge").grid(row=0,column=2,padx=10)
    del_frame.pack(pady=3)

    tk.Button(dash, text="Refresh Table", font=("Arial", 10), command=refresh_table, bg="#b7e8b8", relief="ridge").pack(pady=7)

    # ---------- Change Password feature ----------
    pchange_frame = tk.Frame(dash, bg="#f3f8fa")
    tk.Label(pchange_frame, text=f"Change password for '{loggedin_user}':", font=("Arial", 10), bg="#f3f8fa").grid(row=0,column=0,padx=4,pady=7)
    newpass = tk.Entry(pchange_frame, width=15, show="*")
    newpass.grid(row=0,column=1)
    def chpw():
        npw = newpass.get()
        if not npw:
            messagebox.showwarning("Input", "Enter new password.", parent=dash)
            return
        conn = mysql.connector.connect(host="localhost", user="root", password="10382", database="LoginDemo")
        cur = conn.cursor()
        cur.execute("UPDATE users SET password=%s WHERE username=%s", (npw, loggedin_user))
        if cur.rowcount>0:
            messagebox.showinfo("Password Updated", "Password changed successfully!", parent=dash)
            refresh_table()
        else:
            messagebox.showerror("Error", "Could not update password.", parent=dash)
        conn.commit(); cur.close(); conn.close()
        newpass.delete(0,"end")
    tk.Button(pchange_frame, text="Update Password", font=("Arial", 10), command=chpw, bg="#fed97f", relief="ridge").grid(row=0,column=2,padx=8)
    pchange_frame.pack(pady=5)

# ---------- LOGIN PAGE -----------
def login():
    uname = entry_user.get()
    pwd = entry_pass.get()
    conn = mysql.connector.connect(host="localhost", user="root", password="10382", database="LoginDemo")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
    res = cur.fetchone()
    cur.close(); conn.close()
    if res:
        messagebox.showinfo("Login Success", f"Welcome, {uname}!", parent=root)
        root.configure(bg="#d4f7d4")
        title_label.config(text=f"Hello, {uname}!", fg="#297d43", bg="#d4f7d4")
        show_dashboard(uname)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.", parent=root)
        root.configure(bg="#f7d4d4")
        title_label.config(text="Login Failed 😢", fg="#a52a2a", bg="#f7d4d4")

def signup():
    uname = entry_user.get()
    pwd = entry_pass.get()
    if not uname or not pwd:
        messagebox.showwarning("Input", "Enter username and password.", parent=root)
        return
    conn = mysql.connector.connect(host="localhost", user="root", password="10382", database="LoginDemo")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, pwd))
        conn.commit()
        messagebox.showinfo("Signup Success", "Signup successful! You can now login.", parent=root)
        root.configure(bg="#f7f4d4")
        title_label.config(text="Signup Successful 🎉", fg="#297d43", bg="#f7f4d4")
    except:
        messagebox.showerror("Signup Failed", "Username already taken!", parent=root)
        root.configure(bg="#f7d4d4")
        title_label.config(text="Signup Failed 😢", fg="#a52a2a", bg="#f7d4d4")
    cur.close(); conn.close()

root = tk.Tk()
root.title("✨ LOGIN PAGE | PYTHON + SQL PROJECT ✨")
root.geometry("420x380")
root.configure(bg="#e7f0fd")

title_label = tk.Label(root, text="Welcome to Secure Login Portal", font=("Arial Bold", 18), bg="#e7f0fd", fg="#297d43")
title_label.pack(pady=18)

frame = tk.Frame(root, bd=3, relief="groove", bg="#fafeff")
frame.place(relx=0.5, rely=0.52, anchor="center")

tk.Label(frame, text="Username:", font=("Arial", 12), bg="#fafeff").grid(row=0, column=0, padx=14, pady=10)
entry_user = tk.Entry(frame, font=("Arial", 12), width=20)
entry_user.grid(row=0, column=1, padx=8, pady=10)

tk.Label(frame, text="Password:", font=("Arial", 12), bg="#fafeff").grid(row=1, column=0, padx=14, pady=10)
entry_pass = tk.Entry(frame, show='*', font=("Arial", 12), width=20)
entry_pass.grid(row=1, column=1, padx=8, pady=10)

btn_login = tk.Button(frame, text="🔒 Login", font=("Arial", 12), bg="#99cfff", fg="white",
                      width=17, command=login)
btn_login.grid(row=2, column=0, pady=18, padx=8)

btn_signup = tk.Button(frame, text="📝 Signup", font=("Arial", 12), bg="#91e495", fg="white",
                       width=17, command=signup)
btn_signup.grid(row=2, column=1, pady=18, padx=8)

hint_label = tk.Label(root, text='Demo Login: admin / admin123', font=("Arial", 11), bg="#e7f0fd", fg="#2b2b2b")
hint_label.pack(pady=7)

root.mainloop()