# 🔐 Mini Login System (Python)

Tento projekt je učebný príklad jednoduchého prihlasovacieho systému v Pythone.  
Používa ukladanie používateľov do JSON súboru, hashovanie hesiel so saltom a kontrolu prihlásenia.

---

## ✨ Funkcie
- Registrácia nového používateľa
- Ukladanie údajov do lokálnej JSON databázy
- Hashovanie hesla so saltom (SHA-256)
- Prihlasovanie s kontrolou
- Ochrana proti brute-force (zablokovanie účtu po viacerých pokusoch)

---

## 🧪 Testovací účet
Repo obsahuje ukážkového používateľa:

- **Meno:** `Tester`  
- **Heslo:** `Test123`

Tento účet je v `users.json` a môžeš ho použiť na okamžité vyskúšanie prihlasovania.

---

## 🚀 Spustenie
1. Uisti sa, že máš nainštalovaný **Python 3.10+**.
2. Naklonuj repozitár:
   ```bash
   git clone https://github.com/<tvoje_repo>.git