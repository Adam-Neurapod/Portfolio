import json
import os
import re
import secrets
import hashlib
from datetime import datetime, timedelta

def _parse_dt(dt_str: str | None): return datetime.fromisoformat(dt_str) if dt_str else None

DB_FILE = "users.json"
import os
print("DB PATH:", os.path.abspath(DB_FILE))

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump ({"users": {}}, f, ensure_ascii=False, indent= 2) 
    with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)

def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def validate_password(pw: str) -> tuple[bool, str]:
    "Pravidlá:"
    "-min. 8 znakov"
    "-aspoň 1 číslo"
    "-aspoň 1 veľké písmeno"
    "-aspoň 1 malé písmeno"

    if len(pw) < 8:
        return False, "Heslo musí mať aspoň 8 znakov"
    if not re.search(r"[0-9]", pw):
        return False, "Heslo musí obsahovať aspoň 1 číslo"
    if not re.search(r"[A-Z]", pw):
        return False, "Heslo musí obsahovať aspoň 1 veľké písmeno"
    if not re.search(r"[a-z]", pw):
        return False, "Heslo musí obsahovať aspoň 1 malé písmeno"
    return True, "OK"

def gen_salt(n_bites: int = 16) -> str:
    "Vygeneruj náhodný salt v hex tvare"
    return secrets.token_hex(n_bites)

def hash_password(password: str, salt: str) -> str:
    "Spojí salt + heslo a vytvorí SHA256 hash"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

def register_user(db):
    db = load_db()
    users = db.get("users", {})
    if not isinstance(users, dict):
        users = {}
    username = input("Zadaj použivateľské meno: ").strip().lower()
    if not username:
        print("Meno nemôže byť prázdne")
        return
    pw1 = input("Zadaj heslo")
    pw2 = input("Zopakuj heslo")

    if pw1 != pw2:
        print("Heslá sa nezhodujú")
        return
    ok, msg = validate_password(pw1)
    if not ok:
        print(f"! {msg}")
        return

    if username in users:
        print("Toto meno už existuje. Skús iné.")
        return
    salt = gen_salt()
    pw_hash = hash_password(pw1, salt)
    users[username] = {
        "salt": salt,
        "password_hash": pw_hash,
        "falled_attempts": 0,
        "locked_untill": None
    }
    db["users"] = users
    save_db(db)
    print("Použivateľ '{username}' uložený do users.json")

def login_user(db):
    db = load_db()
    users = db.get("users", {})

    username = input("Zadaj používateľské meno: ").strip().lower()
    user = users.get(username)
    if not user:
        print("Použivateľ neexistuje")
        return
    
    now = datetime.utcnow()
    locked_until = _parse_dt(user.get("locked_until"))
    if locked_until and now < locked_until:
        remaining = locked_until - now
        mins = remaining.seconds // 60
        secs = remaining.seconds % 60
        print(f"Učet je zamknutý ešte {mins} min {secs} s.")
        return
    password = input("Zadaj heslo:")

    salt = user["salt"]
    cantidate_hash = hash_password(password, salt)
    good_hash = user["password_hash"]

    if cantidate_hash == good_hash:
        user["failed_attempts"] = 0
        user["locked_until"] = None
        save_db(db)
        print(f"Vitaj {username}!")
        return
    
    attempts = int(user.get("failed_attempts", 0)) + 1
    user["failed_attempts"] = attempts

    if attempts >= MAX_ATTEMPTS:
        user["failed_attempts"] = 0
        user ["locked_until"] = (now + timedelta(minutes=LOCK_MINUTES)).isoformat()
        save_db(db)
        print(f"Zlé heslo. Učet zamknutý na {LOCK_MINUTES} minút.")
        return
    
    save_db(db)
    left = MAX_ATTEMPTS - attempts
    print(f"Zlé heslo. Zostávajú {left} pokusy.")

def main():
    db = load_db()

    while True:
        print("\n === Mini login CLI ===")
        print("1) Registrácia")
        print("2) Prihlásenie")
        print("0) Koniec")
        choice = input("Voľba:").strip()

        if choice == "0":
            print ("Maj sa!")
        elif choice == "1":
            register_user(db)
        elif choice == "2":
            login_user(db)
        else:
            print("Táto voľba volačo...")

if __name__ == "__main__":
    main()