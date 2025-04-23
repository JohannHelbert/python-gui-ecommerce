import sqlite3
import hashlib


def create_user_table():
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              password_hash TEXT
              )
""")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def registriere_user(username, password):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        print(f"Benutzer {username} erfolgreich registriert.")
    except sqlite3.IntegrityError:
        print("Benutzername bereits vergeben.")
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        print(f"Login erfolgreich. Willkommen, {username}!")
        return True
    else:
        print("Login fehlgeschlagen.")
        return False


if __name__ == "__main__":
    create_user_table()

    # Registrierung
    registriere_user("johann", "geheim123")

    # Login testen
    login_user("johann", "geheim123")  # sollte erfolgreich sein
    login_user("johann", "falsch")     # sollte fehlschlagen
