import tkinter as tk
okno = tk.Tk()
okno.configure(bg="#1e1e1e")
okno.title("Stonemill - Digitálny sprievodca")
okno.geometry("500x300")

popis = tk.Label(okno, text="Vitaj v Stonemille, opýtaj sa na čokoľvek:", fg="white", bg="#1e1e1e", font=("Segoe UI", 12))
popis.pack(pady=10)

vstup = tk.Entry(okno, width=50, bg="#2d2d2d", fg="white", font=("Segoe UI", 11))
vstup.pack()

def odpovedz_na_otazku():
    otazka = vstup.get().lower().strip()
   
    if not otazka:
        vystup.insert(tk.END, "Skúste sa ma na niečo opýtať! \n")
        return
    
    if otazka in ["koniec", "zbohom", "dakujem"]:
        vystup.insert(tk.END, "Vdaka za otázky, príjemný deň v Stonemille! \n")
        return

    elif ("radnice" in otazka or "radnica" in otazka or "radnici" in otazka or "radnicu" in otazka) and ("hodiny" in otazka or "hodín" in otazka or "otváracie" in otazka or "otvorené" in otazka or "otvorená" in otazka or "otváracia" in otazka):
        vystup.insert(tk.END, "Radnica je otvorená každý pracovný deň od 8:00 do 16:00. V našej radnici Vás nebude limitovať ani žiadna prestávka, pretože je plne automatizovaná. \n")
    elif ("turistické centrum" in otazka or "turistickému centru" in otazka or "turistické" in otazka or "informácie pre turistov" in otazka) and ("kde" in otazka or "nachádza" in otazka or "nájdem" in otazka or "umiestnené" in otazka or "nájsť" in otazka):
        vystup.insert(tk.END, "Turistické centrum sa nachádza hned oproti radnici na Conorovom námestí. \n")
    elif ("parkovanie" in otazka or "parkovať" in otazka or "parkovaním" in otazka or "zaparkujem" in otazka or "zaparkovať" in otazka or "parkujú" in otazka) and ("kde" in otazka or "ako" in otazka or "môžem" in otazka):
        vystup.insert(tk.END, "Parkovanie je možné na odstavných parkoviskách na okraji mesta, odkadiaľ sa pohodlne dostanete do mesta našou dopravou. V centre mesta sú taktiež parkoviská, ktoré sú ale pre turistov spoplatnené \n")
    elif ("parkovanie" in otazka or "parkovať" in otazka or "parkovaním" in otazka or "zaparkujem" in otazka or "zaparkovať" or "parkujú" in otazka) and ("spoplatnené" in otazka or "platené" in otazka or "popatok" in otazka):
        vystup.insert(tk.END, "Parkovanie v Stonemille je spoplatnené len v centre mesta a to sumou 1-euro na hodinu. Odstavné parkoviská na okraji mesta sú zadarmo \n")
    elif ("mhd" in otazka or "mestská doprava" in otazka or "doprava" in otazka or "mestská hromadná doprava" in otazka or "mestskú dopravu" in otazka or "verejná doprava" in otazka or "verejnú dopravu" in otazka or "verejnej dopravy" in otazka or "metro" in otazka or "metra" in otazka or "autobusy" in otazka or "autobusov" in otazka or "autobusu" in otazka or "autobus" in otazka or "vlaky" in otazka or "vlak" in otazka or "vlakov" in otazka):
        vystup.insert(tk.END, "MHD v Stonemille funguje z odstavných parkovísk na spôsob kyvadlovej dopravy. Môžete využiť autobusy ktoré jadzia každých 15 minút alebo metro každých 30 minút. V centre mesta je to podobné a MHD má svoje pravidelné linky. Pár minút chôdze od Conorovho námestia na Spokovej ulici sa nachádza vlakové nádražie. \n")
    elif ("lístok" in otazka or "cena lístka" in otazka or "zapatím za lístok" in otazka or "cena mestskej dopravy" in otazka or "koľko stojí" in otazka):
        vystup.insert(tk.END, "Cena lístka je 1-euro na 60 minút pre autobus a 1,50 na 60 minút pre metro. Lístok z odstavného parkoviska na okraji mesta na hlavnú stanicu je zadarmo. \n")
    elif (
            ("čo vidieť" in otazka or
            "kam ísť" in otazka or
            "zaujímavosti" in otazka or
            "atrakcie" in otazka or
            "výlet" in otazka or
            "navštíviť" in otazka or
            "tipy" in otazka) and
            not "zaujímavosti v okolí" in otazka and
            not "čo vidieť v okolí" in otazka and
            not "okolí" in otazka
        ):
        vystup.insert(tk.END, "V stonemille sa určite oplatí navštíviť, staré mesto, múzeum umelej inteligencie, park aurora, alebo galériu svetelných projekcii. Vždy je tu čo vidieť! \n")
    elif (
            "historické centrum" in otazka or
            "staré mesto" in otazka or
            "kamenné uličky" in otazka or
            "zvonica" in otazka or
            "centrum" in otazka or
            "starom meste" in otazka
        ):
        vystup.insert(tk.END, "Historické centrum Stonemillu je známe svojimy kamennými uličkami, zvonicou z konca 12. storočia a krásnou atmosférou starého mesta ktorá sa miesy s modernými technologiami. \n")
    elif (
            "muzeum" in otazka or
            "múzeum" in otazka or
            "inteligencie" in otazka or
            "AI múzeum" in otazka or
            "umelej inteligencie" in otazka or
            "ai múzeum" in otazka
        ):
        vystup.insert(tk.END, "Múzeum umelej inteligencie v Stonemille ponúka jedinečný zážitok a ukážku ako AI pomáhala budovať naše mesto. Dozviete sa celú historiu od prvého kódu až po digitálne prepojenie ako ho vidíme dnes. \n")
    elif (
            ("park aurora" in otazka or
            "lesný park" in otazka or
            "Aurora" in otazka or
            "aurora" in otazka or
            "parku" in otazka) and
            not "reštaurácia" in otazka and
            not "ponúka" in otazka and
            not "menu" in otazka and
            not "jedlo" in otazka
        ):
        vystup.insert(tk.END, "Lesný park Aurora je ideálne miesto na oddych v korunách stromov, svetelnými inštaláciami, občerstvením a mnohým dalším. V srdci parku môžete nájsť jeden z prvých vesmírnych AI satelitov podla ktorého park nesie svoje meno. \n")
    elif (
            "výstava robotov" in otazka or
            "výstava" in otazka or
            "robotov" in otazka or
            "robotmi" in otazka or
            "retro robotov" in otazka or
            "retro robotmi" in otazka
        ):
        vystup.insert(tk.END, "Stonemill ponúka aj svoju jedinečnú výstavu retro robotov kde môžete vidieť a na vlastné oči zažiť rozhovor s prvým modelom AI robota, dalej možete vidieť prvých robotických pomocníkov, modeli robotov ako bol F100 a mnoho iného. \n")
    elif (
            "čo ponúka Neuron byte" in otazka or
            "reštaurácia neuron byte" in otazka or
            "kde sa nachádza neuron byte" in otazka or
            "čo ponúka reštaurácia neuron byte" in otazka or
            "neuron byte" in otazka
        ):
        vystup.insert(tk.END, "Rešťaurácia Neuron byte sa nachádza na Conorovom námestí. V ponuke nájdete napríklad Plasma tacos, veľmi obľúbený Quantum burger a mnoho daľšieho. \n")
    elif (
    "reštaurácia aurora" in otazka or
    "čo ponúka reštaurácia aurora" in otazka or
    "ponuka reštaurácie aurora" in otazka or
    "ponuka reštaurácie aurora" in otazka or
    "ponuka v aurora dine" in otazka or
    "aurora dine menu" in otazka
        ):
        vystup.insert(tk.END, "V Aurora dine nájdete príjemnú atmosféru parku Aurora a skvelé jedlo. V ponuke je napríklad photon salad, AI rissoto a vyhľadávaný nebula sorbet. \n")
    elif (
            "reštaurácie" in otazka or
            "občerstvenie" in otazka or
            "jedlo" in otazka or
            "tradičné jedlá" in otazka or
            "reštaurácia" in otazka or
            "kam na jedlo" in otazka or
            "kam ísť jesť" in otazka or
            "kde sa najesť" in otazka or
            "kde varia" in otazka or
            "kde sa najem" in otazka
        ):
        vystup.insert(tk.END, "V Stonemille sa nachádza hned niekoľko reštaurácii kde určite nájdete niečo presne pre Vás. V podniku Neuron byte môžete čakať digitálnu atmosferu a holografických čašníkov. V Aurora dine naopak elegantnú panoarmatickú atmosféru uprostred parku Aurora. \n")
    elif (
            ("ubytovanie" in otazka or
            "hotel" in otazka or
            "prenocovanie" in otazka or
            "prenocovať" in otazka or
            "ubytovať" in otazka or
            "hoteli" in otazka or 
            "hotela" in otazka or
            "možnosti ubytovania" in otazka or
            "kde prespať" in otazka or
            "kde sa ubytovať" in otazka) and
            not "quantum nest" in otazka and
            not "starfield" in otazka and
            not "capsule" in otazka and
            not "neuron" in otazka
        ):
        vystup.insert(tk.END, "V Stonemile nájdete rôzne možnosti ubytovania podľa toho čo preferujete- od digitálneho luxusu v hoteli Quantum Nest na Neon street až po pokonjný Starfield Capsule Hotel v Severnej štvrti. \n")
    elif (
            ("hoteli quantum nest" in otazka or
            "cenník hotela quantum nest" in otazka or
            "aká je cena za noc v hoteli" in otazka or
            "cena za noc" in otazka or
            "koľko stojí" in otazka) and
            not "ubytovanie v quantum nest" in otazka and
            not "hotel quantum nest" in otazka and
            not "ubytovanie" in otazka
        ):
         vystup.insert(tk.END, "Cena za noc v Hoteli Quantum nest sa pohybuje od 130-eur za noc v základnej izbe až po 400-eur za noc v najluxusnejšej izbe ktorá ponúka zážitok ako z iného sveta! \n")
    elif (
            "quantum nest" in otazka or
            "hotel quantum nest" in otazka or
            "kde je quantum nest" in otazka or
            "čo ponúka quantum nest" in otazka
        ):
        vystup.insert(tk.END, "Hotel Quantum Nest sa nachádza na Neon street, v srdci digitálne štvrte. Nájdete tu luxusné izby s AR oknami, AI concierge a nočnú projekciu galaxie priamo nad hlavou. \n")
    elif (
            ("starfield capsule" in otazka or
             "hotel starfield capsule" in otazka or
             "kapsulový hotel" in otazka) and
             ("cena" in otazka or
              "cena za noc" in otazka or
              "koľko stojí" in otazka or
              "cenník" in otazka)
        ):
        vystup.insert(tk.END, "Ceny v Hoteli Starfield Capsule sa pohybujú od 30-eur za noc pre základnú izbu až po 60-eur za noc v najlepšie vybavenej izbe. \n")
    elif (
            "starfield capsule" in otazka or
            "starfield capsule hotel" in otazka or
            "kapsulový hotel" in otazka or
            "ubytovanie v starfield hotel" in otazka or
            "ubytovanie v starfield" in otazka
        ):
        vystup.insert(tk.END, "Starfield Capsule Hotel je umiestnený v tichej Severnej štvti. Ponúka kompaktné kapsule, nočnú projekciu hviezd a digitálne relax zóny s AI masážou. \n")
    elif (
            "zdravotne stredisko" in otazka or
            "klinika" in otazka or
            "zdravotná starostlivosť" in otazka or
            "pohotovosť" in otazka or
            "zdravotná pomoc" in otazka or
            "lekár" in otazka or
            "ambulancia" in otazka or
            "nemocnica" in otazka
        ):
        vystup.insert(tk.END, "V meste Stonemill sa nachádza plne vybavená nemocnica Medicore hospital, ktorá sa nachádza pri hlavnej dopravnej tepne nedaleko mesta.Tiež sa môžete spolahnúť na dve plne digitalizované ambulancie Medicore healing pot v Severnej štvrti a nedaleko Conorovho námestia. \n")
    elif (
            "okolie" in otazka or
            "zaujímavosti v okolí" in otazka or
            "čo vidieť v okolí" in otazka or
            "okolí" in otazka or
            "turistika v okolí" in otazka
        ):
        vystup.insert(tk.END, "V okolí Stonemillu nájdeš digitálne observatórium, staré bane premenené na múzeum robotického baníctvaa lesnú zónu so solárnými vyhliadkami. Všetko ideálne na krátke výlety po okolí. \n")
    elif (
            "digitálne služby mesta" in otazka or
            "mestská aplikácia" in otazka or
            "smart aplikácia" in otazka or
            "smart riešenia" in otazka or
            "kiosk" in otazka
        ):
        vystup.insert(tk.END, "Stonemill ponúka celú radu smart riešení. Priamo tu na informáciach si môžete oskenovaním QR kódu stiahnuť mestkú aplikáciu Smartmill kde nájdete prehľad o všetkých novinkách mesta, podujatiach, zajednať ubytovanie a mnoho dalšieho. Cez aplikáciu Smartmill, zvládnete všetko čo v našom meste potrebujete. \n")
    elif (
            "všetko" in otazka or
            "koniec" in otazka or
            "dakujem" in otazka or
            "to je asi všetko" in otazka or
            "to je všetko" in otazka or
            "už nič" in otazka or
            "dovidenia" in otazka or
            "ahoj" in otazka
        ):
        vystup.insert(tk.END, "Som rád, že som mohol pomôcť! Prajem krásny deň v Stonemille, meste kde sa minulosť stretáva s budúcnosťou. Ak budeš niečo potrebovať, som tu pre teba! \n")
    else:
        vystup.insert(tk.END, "Prepáč, tejto otázke zatiaľ nerozumiem. Skús sa opýtať inak, alebo použi jednu z hlavných tém ako doprava, zaujímavosti, ubytovanie a podobne. \n")

tlacidlo = tk.Button(okno, text="Opýtať sa", command= odpovedz_na_otazku, bg="#007acc", fg="white", font=("Segoe UI", 11, "bold"))
tlacidlo.pack(pady=10)

scrollbar = tk.Scrollbar(okno)
vystup = tk.Text(okno, height=8,
                 width=60, bg="#121212", fg="white", font=("Consolas", 11), wrap="word", yscrollcommand=scrollbar.set)
scrollbar.config(command=vystup.yview)
vystup.pack(side=tk.LEFT)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

okno.mainloop()