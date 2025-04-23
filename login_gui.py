import tkinter as tk
from tkinter import messagebox
import nutzer_db
import shop_gui
import nutzer_db
nutzer_db.create_user_table()


def versuche_login():
    benutzername = entry_user.get()
    passwort = entry_pass.get()

    if nutzer_db.login_user(benutzername, passwort):
        messagebox.showinfo("Login erfolgreich",
                            f"Willkommen, {benutzername}!")
        root.destroy()  # Loginfenster schließen

    else:
        messagebox.showerror("Fehler", "Benutzername oder Passwort falsch.")

    shop_gui.start_shop()


root = tk.Tk()
root.title("Login")
root.geometry("300x200")

label_user = tk.Label(root, text="Benutzername:")
label_user.pack(pady=5)

entry_user = tk.Entry(root)
entry_user.pack(pady=5)

label_pass = tk.Label(root, text="Passwort:")
label_pass.pack(pady=5)

entry_pass = tk.Entry(root, show="*")  # Passwort wird versteckt
entry_pass.pack(pady=5)

login_button = tk.Button(root, text="Login", command=versuche_login)
login_button.pack(pady=20)

root.mainloop()
