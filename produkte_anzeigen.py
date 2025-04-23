import tkinter as tk
import sqlite3
from tkinter import messagebox


def lade_produkte():
    connection = sqlite3.connect("shop.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    produkte = cursor.fetchall()
    connection.close()
    return produkte


# GUI erstellen
root = tk.Tk()
root.title("Produktliste")
root.geometry("400x300")

produkte = lade_produkte()

for produkt in produkte:
    name = produkt[1]
    preis = produkt[2]
    lager = produkt[3]
    frame = tk.Frame(root)
    frame.pack(anchor="w", pady=5)

    label = tk.Label(
        frame, text=f"{name} - {preis}€ ({lager} Stück)", width=30, anchor="w")
    label.pack(side="left")

    button = tk.Button(frame, text="In den Warenkorb",
                       command=lambda pid=produkt[0]: zum_warenkorb_hinzufügen(pid))
    button.pack(side="right")


warenkorb = []  # Liste für Produkte im Warenkorb


def zum_warenkorb_hinzufügen(produkt_id):
    connection = sqlite3.connect("shop.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, price FROM products WHERE id=?", (produkt_id,))
    produkt = cursor.fetchone()
    connection.close()

    if produkt:
        warenkorb.append(produkt)
        print(f"{produkt[0]} zum Warenkorb hinzugefügt.")


def zeige_warenkorb():
    fenster = tk.Toplevel(root)
    fenster.title("Warenkorb")

    def aktualisiere_warekorb():
        for widget in fenster.winfo_children():
            widget.destroy()  # Alles im Fenster löschen und neu zeichen

        gesamtpreis = 0.0

        for index, produkt in enumerate(warenkorb):
            name, preis = produkt

            frame = tk.Frame(fenster)
            frame.pack(anchor="w", pady=2)

            label = tk.Label(
                frame, text=f"{name} - {preis}€", width=30, anchor="w")
            label.pack(side="left")

            entferne_button = tk.Button(
                frame,
                text="🗑 Entfernen",
                command=lambda i=index: entferne_aus_warenkorb(
                    i, aktualisiere_warekorb)
            )
            entferne_button.pack(side="right")

            gesamtpreis += preis

        gesamt_label = tk.Label(
            fenster, text=f"Gesamtpreis: {gesamtpreis:2f}€", font=("Arial", 12, "bold"))
        gesamt_label.pack(pady=10)

    def entferne_aus_warenkorb(index, callback):
        del warenkorb[index]  # Produkt aus Liste löschen
        callback()  # GUI neu zeichnen

    aktualisiere_warekorb()

    if warenkorb:
        bezahlen_button = tk.Button(
            fenster,
            text="💳 Zahlung abschließen",
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            command=lambda: bezahle(fenster, aktualisiere_warekorb)
        )
        bezahlen_button.pack(pady=10)

    def bezahle(fenster, callback):
        warenkorb.clear()
        callback()
        tk.messagebox.showinfo(
            "Bezahlung", "✅ Zahlung erfolgreich! Vielen Dank für deinen Einkauf.")


warenkorb_button = tk.Button(
    root, text="🛒 Warenkorb anzeigen", command=zeige_warenkorb)
warenkorb_button.pack(pady=10)


root.mainloop()
