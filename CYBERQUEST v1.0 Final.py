import re

lokacie = {
    "strecha":{
        "popis": "Stojíš na opustenej streche zničeného komplexu. V diaľke blikajú neónové nápisy a elektrické búrky rozžiaria horizont. Na juh vedú staré schody dole.", "vychody": {"juh": "schodisko"}},
        "schodisko": {
            "popis": "Oceľové schodisko klesá do tmy a vrzga pod každým krokom. Zo severu vedie cesta späť na strechu, na juh ide do tmavej ulice", "vychody": {"sever": "strecha", "juh": "ulica"}},
            "ulica": {
                "popis": "Kráčaš úzkou tmavou uličkou, kde sa medzi vysokými budovami sa drží hustý smog. Na stenách blikajú pokazené neónové reklamy a rozbité svetlá osvetľujú len zlomky cesty."
                "Vzduch páchne olejom a ozýva sa vzdialený hukot generátorov. Niektoré dvere sú zamknuté, no na juh vedie nenápadný vchod do skladu.", "vychody": {"sever": "schodisko", "juh": "sklad"}},
                "sklad": {
                    "popis": "Ocitáš sa vo vlkhom sklade plnom roztrúsených debien a zaprášených súčiastok. Vzduch je ťažký a nasiaknutý pachom starej elektroniky a plesne."
                    "Tlmené svetlá nad hlavou slabnú, akoby sa každú chvíľu maly vypariť. Na juh vedú schody dole, do podzemného tunela pod skladom. Na severe vidíš východ spať do ulice.", "vychody": {"sever": "ulica", "dole": "tunel_sklad"}},
                    "tunel_sklad": {
                        "popis": "Podzemný tunel s blikajúcim núdzovým svetlom. Steny sú plné káblov a na konci tunela vidieť hrdzavé dvere do skrytého vchodu. Smerom na juh...", "vychody": {"hore": "sklad", "juh": "skrity_port"}},
                        "skrity_port": {
                            "popis": "Našiel si skritý port, kedysi ho využívali pašeráci a podzemné frakcie. Kovové dvere s vyblednútymi symbolmi sa ešte stále dajú otvoriť. Cítiť tu zvláštny pokoj ale aj riziko -"
                            "odtiaľto môžeš uniknúť do útočiska za mestom, no zároveň je tu východ dole, ktorý vedie ešte hlbšie do temných tunelov. Každé rozhodnutie ktoré tu spravíš, sa môže vymknúť spod konroly.", "vychody": {"dole": "tunel_port", "von": "utocisko"}},
                            "tunel_port": {
                                "popis": "Podzemný tunel s blikajúcimi svetlami. Na konci sú masívne dvere vedúce dole, do technického uzla", "vychody": {"dole": "uzol_kontroly"}},
                                "uzol_kontroly": {
                                    "popis": "Si vo vnútri hlavného uzla kontroly. Masívna miestnosť plná serverov, blikajúcich terminálov a neónových panelov, ktoré vyžarujú slabé, hypnotické svetlo. Vdzuch tu vybruje od bzukotu strojov"
                                    "a cyklických záznamov starých systémov. Každý pohyb ti pripomína, že tu už dávno nemal nikto vkročiť. Zdanlivo nekonečný labyrint káblov vedie k centrálnej konzole, ktorá drží kontrolu nad celým komplexom."
                                    "toto miesto sa zdá byť hlboko prepojené so všetkým, čo sa v meste ešte hýbe.", "vychody": {},
                                    "zamknute": False
                                    }
                                    }

debug_mode = False
def rozpoznaj_prikaz(text):
    import re
    vzor_pohyb = re.compile(r"(choď|chod|presuň sa|pohybuj sa|)( na| smer)? (sever|juh|západ|východ|dole|hore)", re.IGNORECASE)
    zhodne = vzor_pohyb.search(text)
    if zhodne:
        return ("pohyb", zhodne.group(3))
    elif re.search(r"(pozri sa|preskumaj|rozhliadni sa)", text, re.IGNORECASE):
        return ("pozri_sa", None)
    elif re.search(r"(hackuj|hackni|odomkni)", text, re.IGNORECASE):
        return ("hackuj", None)
    else:
        return ("neznamy", None)
cesta = ["strecha"]
aktualna_lokacia = "strecha"
print("\n" + "=" * 40)
print("          C Y B E R Q U E S T")
print("     (verzia 1.0 - by Neurapod Team)")
print("=" * 40)
print("\nVitaj v temnej cyberpunk adventúre.")
print("Tvoje rozhodnutia určia tvoj osud.")
print("Napíš príkaz a urči svoje putovanie.")
print("=" * 40)

while True:
        print("\n>> Presúvaš sa...")
        print(f"\n>> Nachádzaš sa na mieste: {aktualna_lokacia.upper()}")
        print(f"{lokacie[aktualna_lokacia]['popis']}")
        prikaz = input("\n>> Zadaj príkaz: ")
        if prikaz.lower() in ["ukončiť", "ukonči", "skonči", "koniec", "končím", "exit",]:
            print(">>Hra ukončená.")
            break

        akcia, smer = rozpoznaj_prikaz(prikaz)
        if debug_mode:
            print(f"DEBUG: akcia={akcia}, smer={smer}")
        if akcia == "pohyb":
            slovnik_miestnosti = lokacie
            miestnost = slovnik_miestnosti.get(aktualna_lokacia, None)
            for cast in cesta:
                if debug_mode:
                    print(f"DEBUG: Prechadzam cez cestu: {cesta}, aktualne {cast}")
                miestnost = slovnik_miestnosti.get(cast, None)
                if debug_mode:
                    print(f"DEBUG: Miestnost keys: {list(miestnost.keys()) if miestnost else 'None'}")
                if miestnost is None:
                    print(f">>Chyba: Miestnosť '{cast}' sa nenašla. Končím hľadanie.")
                    break
                else:
                    if "vychody" in miestnost:
                        if smer in miestnost["vychody"]:
                            nova_lokacia = miestnost["vychody"][smer]
                            if "zamknute" in slovnik_miestnosti.get(nova_lokacia, {}) and slovnik_miestnosti[nova_lokacia]["zamknute"]:
                                print(">>Dvere sú zamknuté. Najskôr ich musíš hacknúť.")
                            else:
                                if nova_lokacia not in cesta:
                                    cesta.append(nova_lokacia)
                                    aktualna_lokacia = nova_lokacia
                                    break
                                else:
                                    if debug_mode:
                                        print(f"DEBUG: Aktualna miestnosť: {aktualna_lokacia}")
                                    print(">> Týmto smerom sa nedá dostať.")
                    elif akcia == "pozri sa":
                        print(f">>{lokacie[aktualna_lokacia]['popis']}")
                    else:
                        print(">>Nerozpoznaný príkaz.")
        elif akcia == "hackuj":
            for cast in cesta:
                miestnost = lokacie
                if not miestnost:
                    print(f">>Chyba: Miestnosť '{cast}' sa nenašla v ceste. Končím hľadanie.")
                    break
                if "vychody" in miestnost:
                    if debug_mode:
                        print(f"DEBUG: Miestnosť má východy: {miestnost['vychody']}")
                else:
                    if debug_mode:
                        print(f"DEBUG: Miestnosť nemá východy")
                    if "zamknute" in miestnost and miestnost["zamknute"]:
                        miestnost["zamknute"] = False
                        print(f">>Hackovanie úspešné, dvere sú odomknuté.")
                    else:
                        (f">>Tu nie je nič čo by sa dalo hacknúť.")
            else:
                print(">>Nerozpoznaný príkaz.")