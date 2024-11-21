import json


class AdatKezeles:
    """
    Adatbázis kezelő osztály, amely felelős a JSON fájl betöltéséért és az adatok tárolásáért.
    """
    adatok = {}
    ADATBAZIS_FAJL = "iskola_adatbazis.json"

    @staticmethod
    def adatok_betoltese():
        """
        Betölti az iskola_adatbazis.json fájlt és eltárolja az adatokat az osztály adatok attribútumában.
        """
        with open(AdatKezeles.ADATBAZIS_FAJL, "r", encoding="utf-8") as f:
            AdatKezeles.adatok = json.load(f)


AdatKezeles.adatok_betoltese()


class Tanev:
    """
    A tanév kezelésért felelős osztály, amely az aktuális tanév adatait kezeli.
    """
    @staticmethod
    def tanev():
        """
        Kiírja az aktuális tanév adatait és az utolsó frissítés dátumát.
        """
        return print(
            f"Üdvözöllek a {AdatKezeles.adatok['metadata']['tanev']} tanév rendszerében, "
            f"utoljára frissítve: {AdatKezeles.adatok['metadata']['utolso_frissites']}")


class Azonosito:
    """
    Kiírja az aktuális tanév adatait és az utolsó frissítés dátumát.
    """
    @staticmethod
    def get_diak_nev(diak_id):
        """
        Visszaadja a diák nevét az azonosítója alapján.

        Args:
            diak_id (str): A diák egyedi azonosítója

        Returns:
            str: A diák neve
        """
        return AdatKezeles.adatok['diakok'][diak_id]['nev']

    @staticmethod
    def get_tantargy_nev(tantargy_id):
        """
        Visszaadja a tantárgy nevét az azonosítója alapján.

        Args:
            tantargy_id (str): A tantárgy egyedi azonosítója

        Returns:
            str: A tantárgy neve vagy az eredeti azonosító, ha nem található
        """
        for tantargy_kulcs, tantargy_adat in AdatKezeles.adatok['tantargyak'].items():
            if tantargy_adat['id'] == tantargy_id:
                return tantargy_adat['nev']
        return tantargy_id


class Tanarok:
    """
    A tanárok kezelésért felelős osztály, amely tartalmazza a tanárokkal kapcsolatos műveleteket.
    """
    @staticmethod
    def tanarok_listazasa():
        """
        Kilistázza az összes tanár adatait részletesen, beleértve a személyes információkat,
        tanított tantárgyakat és osztályokat.
        """
        for tanar_id, tanar_adatok in AdatKezeles.adatok["tanarok"].items():
            print(f"\nTanár azonosító: {tanar_id}")
            print(f"Név: {tanar_adatok['nev']}")
            print(f"Születési dátum: {tanar_adatok['szuletesi_datum']}")
            print(f"Végzettség: {tanar_adatok['vegzettseg']}")
            print(f"Email: {tanar_adatok['email']}")
            print(f"Telefonszám: {tanar_adatok['telefonszam']}")
            if 'tantargyak' in tanar_adatok:
                print("Tanított tantárgyak:", ', '.join(tanar_adatok['tantargyak']))
            if 'osztalyfonok' in tanar_adatok:
                print(f"Osztályfőnök: {tanar_adatok['osztalyfonok']}")
            if 'tanitott_osztalyok' in tanar_adatok:
                print("Tanított osztályok:", ', '.join(tanar_adatok['tanitott_osztalyok']))
            print("-" * 50)

    @staticmethod
    def uj_tanar_felvetele():
        """
        Új tanár felvétele a rendszerbe. Bekéri a szükséges adatokat és létrehoz egy új tanár bejegyzést.
        Automatikusan generál egyedi azonosítót és email címet.
        """
        print("\nÚj tanár felvétele")
        print("-" * 20)
        nev = input("Add meg a tanár nevét: ")
        szuletesi_datum = input("Add meg a születési dátumot (ÉÉÉÉ-HH-NN): ")
        vegzettseg = input("Add meg a végzettséget: ")
        telefonszam = input("Add meg a telefonszámot: ")
        email = f"{nev.lower().replace(' ', '.')}@iskola.hu"
        tantargyak = []
        print("\nVálassz tanítandó tantárgyakat:")
        print("Elérhető tantárgyak:")
        for tantargy in AdatKezeles.adatok["tantargyak"].keys():
            print(f"- {tantargy}")
        while True:
            tantargy = input("\nAdd meg a tantárgy nevét (vagy 'vege' a befejezéshez): ").lower()
            if tantargy == 'vege':
                break
            if tantargy not in AdatKezeles.adatok["tantargyak"]:
                print("Nem létező tantárgy!")
                continue
            if tantargy not in tantargyak:
                tantargyak.append(tantargy)
                print(f"{tantargy} hozzáadva!")
            else:
                print("Ez a tantárgy már hozzá van rendelve!")
        tanitott_osztalyok = []
        print("\nVálassz tanítandó osztályokat:")
        print("Elérhető osztályok:")
        for osztaly_id in AdatKezeles.adatok["osztalyok"].keys():
            print(f"- {osztaly_id}")
        while True:
            osztaly = input("\nAdd meg az osztály azonosítóját (vagy 'vege' a befejezéshez): ")
            if osztaly == 'vege':
                break
            if osztaly not in AdatKezeles.adatok["osztalyok"]:
                print("Nem létező osztály!")
                continue
            if osztaly not in tanitott_osztalyok:
                tanitott_osztalyok.append(osztaly)
                print(f"{osztaly} hozzáadva!")
            else:
                print("Ez az osztály már hozzá van rendelve!")
        uj_id = f"T{len(AdatKezeles.adatok['tanarok']) + 1:03d}"
        uj_tanar = {
            "id": uj_id,
            "nev": nev,
            "szuletesi_datum": szuletesi_datum,
            "vegzettseg": vegzettseg,
            "telefonszam": telefonszam,
            "email": email,
            "tantargyak": tantargyak
        }
        if tanitott_osztalyok:
            uj_tanar["tanitott_osztalyok"] = tanitott_osztalyok
        AdatKezeles.adatok["tanarok"][uj_id] = uj_tanar
        print(f"\nTanár sikeresen felvéve! (ID: {uj_id})")

    @staticmethod
    def tanar_torlese():
        """
        Tanár törlése a rendszerből. Ellenőrzi, hogy a tanár törölhető-e (nincs osztályfőnöki vagy
        aktív tanítási feladata), majd végrehajtja a törlést.
        """
        print("\nTanár törlése")
        print("-" * 20)
        Tanarok.tanarok_listazasa()
        tanar_id = input("\nAdd meg a törölni kívánt tanár ID-jét: ")
        if tanar_id not in AdatKezeles.adatok["tanarok"]:
            print("Nem létező tanár ID!")
            return
        tanar = AdatKezeles.adatok["tanarok"][tanar_id]
        if 'osztalyfonok' in tanar:
            print("A tanár nem törölhető, mert osztályfőnök!")
            return
        if 'tanitott_osztalyok' in tanar:
            for osztaly_id in tanar['tanitott_osztalyok']:
                osztaly = AdatKezeles.adatok["osztalyok"][osztaly_id]
                for tantargy, adat in osztaly['tantargyak'].items():
                    if adat['tanar_id'] == tanar_id:
                        print(f"A tanár nem törölhető, mert aktívan tanít a {osztaly_id} osztályban!")
                        return
        del AdatKezeles.adatok["tanarok"][tanar_id]
        print("\nTanár sikeresen törölve!")

    @staticmethod
    def tanar_keresese():
        """
        Tanárok keresése különböző szempontok alapján (név, tantárgy, osztály).
        Részletes információkat jelenít meg a találatokról.
        """
        print("\nTanár keresése")
        print("-" * 20)
        print("Keresési opciók:")
        print("1. Név alapján")
        print("2. Tantárgy alapján")
        print("3. Osztály alapján")
        try:
            valasztas = int(input("\nVálassz keresési opciót: "))
            if valasztas == 1:
                nev = input("Add meg a keresett nevet vagy névtöredéket: ").lower()
                talalatok = []
                for tanar_id, tanar in AdatKezeles.adatok["tanarok"].items():
                    if nev in tanar["nev"].lower():
                        talalatok.append(tanar_id)
            elif valasztas == 2:
                tantargy = input("Add meg a tantárgyat: ").lower()
                talalatok = []
                for tanar_id, tanar in AdatKezeles.adatok["tanarok"].items():
                    if 'tantargyak' in tanar and tantargy in tanar["tantargyak"]:
                        talalatok.append(tanar_id)
            elif valasztas == 3:
                osztaly = input("Add meg az osztályt: ")
                talalatok = []
                for tanar_id, tanar in AdatKezeles.adatok["tanarok"].items():
                    if ('tanitott_osztalyok' in tanar and
                            osztaly in tanar["tanitott_osztalyok"]):
                        talalatok.append(tanar_id)
            else:
                print("Érvénytelen választás!")
                return
            if talalatok:
                print("\nTalálatok:")
                for tanar_id in talalatok:
                    tanar = AdatKezeles.adatok["tanarok"][tanar_id]
                    print(f"\nNév: {tanar['nev']}")
                    print(f"ID: {tanar_id}")
                    print(f"Végzettség: {tanar['vegzettseg']}")
                    if 'tantargyak' in tanar:
                        print("Tanított tantárgyak:", ', '.join(tanar['tantargyak']))
                    if 'osztalyfonok' in tanar:
                        print(f"Osztályfőnök: {tanar['osztalyfonok']}")
                    if 'tanitott_osztalyok' in tanar:
                        print("Tanított osztályok:", ', '.join(tanar['tanitott_osztalyok']))
                    print("-" * 30)
            else:
                print("\nNincs találat a keresési feltételeknek megfelelően!")
        except ValueError:
            print("Érvénytelen bemenet!")

    @staticmethod
    def tanar_menu():
        """
        A tanárok kezelésére szolgáló menürendszer.

        Megjeleníti és kezeli a tanárokkal kapcsolatos műveletek menüjét:
        - Új tanár felvétele
        - Tanár törlése
        - Tanárok listázása
        - Tanár keresése
        - Visszatérés a főmenübe
        """
        while True:
            print('----------------------------------------------')
            print('Tanárok Kezelése!')
            print('1. Új Tanár Felvétele.')
            print('2. Tanár Törlése.')
            print('3. Tanár Listázása.')
            print('4. Tanár Keresése.')
            print('5. Vissza a főmenübe')

            try:
                valasztott = int(input('Kérlek válassz a menüpontok közül: '))
                match valasztott:
                    case 1:
                        Tanarok.uj_tanar_felvetele()
                    case 2:
                        Tanarok.tanar_torlese()
                    case 3:
                        Tanarok.tanarok_listazasa()
                    case 4:
                        Tanarok.tanar_keresese()
                    case 5:
                        return
                    case _:
                        print("Érvénytelen választás!")
            except ValueError:
                print("Kérlek számot adj meg!")


class Diakok:
    """
    A diákok kezelésért felelős osztály, amely tartalmazza a diákokkal kapcsolatos műveleteket.
    """
    @staticmethod
    def diakok_listazasa():
        """
        Kilistázza az összes diák adatait részletesen, beleértve a személyes információkat,
        szülők adatait és hiányzásokat.
        """
        for diak_id, diak_adatok in AdatKezeles.adatok["diakok"].items():
            print(f"\nDiák azonosító: {diak_id}")
            print(f"Név: {diak_adatok['nev']}")
            print(f"Születési dátum: {diak_adatok['szuletesi_datum']}")
            print(f"Lakcím: {diak_adatok['lakcim']}")
            if 'osztaly_id' in diak_adatok:
                print(f"Osztály: {diak_adatok['osztaly_id']}")
            print(f"Email: {diak_adatok['email']}")
            print("\nSzülők:")
            print(f"Anya: {diak_adatok['szulok']['anya']['nev']}")
            print(f"  Telefonszám: {diak_adatok['szulok']['anya']['telefonszam']}")
            print(f"  Email: {diak_adatok['szulok']['anya']['email']}")
            if 'apa' in diak_adatok['szulok']:
                print(f"Apa: {diak_adatok['szulok']['apa']['nev']}")
                print(f"  Telefonszám: {diak_adatok['szulok']['apa']['telefonszam']}")
                print(f"  Email: {diak_adatok['szulok']['apa']['email']}")
            print("\nHiányzások:")
            print(f"Igazolt: {diak_adatok['hianyzasok']['igazolt']}")
            print(f"Igazolatlan: {diak_adatok['hianyzasok']['igazolatlan']}")
            print("-" * 50)

    @staticmethod
    def uj_diak_felvetele():
        """
        Új diák felvétele a rendszerbe. Bekéri a személyes adatokat, szülők adatait,
        és opcionálisan osztályhoz rendeli a diákot.
        """
        print("\nÚj diák felvétele")
        print("-" * 20)
        nev = input("Add meg a diák nevét: ")
        szuletesi_datum = input("Add meg a születési dátumot (ÉÉÉÉ-HH-NN): ")
        lakcim = input("Add meg a lakcímet: ")
        telefonszam = input("Add meg a telefonszámot: ")
        email = f"{nev.lower().replace(' ', '.')}@diak.iskola.hu"
        print("\nAnya adatai:")
        anya_nev = input("Név: ")
        anya_telefon = input("Telefonszám: ")
        anya_email = input("Email: ")
        print("\nApa adatai (ha van, egyébként üres):")
        apa_nev = input("Név (üres ha nincs): ")
        szulok = {
            "anya": {
                "nev": anya_nev,
                "telefonszam": anya_telefon,
                "email": anya_email
            }
        }
        if apa_nev:
            apa_telefon = input("Telefonszám: ")
            apa_email = input("Email: ")
            szulok["apa"] = {
                "nev": apa_nev,
                "telefonszam": apa_telefon,
                "email": apa_email
            }
        print("\nElérhető osztályok:")
        for osztaly_id in AdatKezeles.adatok["osztalyok"].keys():
            print(f"- {osztaly_id}")
        osztaly_id = input("\nAdd meg az osztályt (üres ha nincs még osztálya): ")
        if osztaly_id and osztaly_id not in AdatKezeles.adatok["osztalyok"]:
            print("Nem létező osztály!")
            return
        uj_id = f"D{len(AdatKezeles.adatok['diakok']) + 1:03d}"
        uj_diak = {
            "id": uj_id,
            "nev": nev,
            "szuletesi_datum": szuletesi_datum,
            "telefonszam": telefonszam,
            "lakcim": lakcim,
            "email": email,
            "szulok": szulok,
            "hianyzasok": {
                "igazolt": 0,
                "igazolatlan": 0
            }
        }
        if osztaly_id:
            uj_diak["osztaly_id"] = osztaly_id
            AdatKezeles.adatok["osztalyok"][osztaly_id]["diak_ids"].append(uj_id)
            AdatKezeles.adatok["osztalyok"][osztaly_id]["letszam"] += 1
        AdatKezeles.adatok["diakok"][uj_id] = uj_diak
        print(f"\nDiák sikeresen felvéve! (ID: {uj_id})")

    @staticmethod
    def diak_adatainak_modositasa():
        """
        Diák adatainak módosítása. Lehetőséget biztosít személyes adatok, szülők adatai,
        hiányzások és osztály módosítására.
        """
        print("\nDiák adatainak módosítása")
        print("-" * 20)
        Diakok.diakok_listazasa()
        diak_id = input("\nAdd meg a módosítani kívánt diák ID-jét: ")
        if diak_id not in AdatKezeles.adatok["diakok"]:
            print("Nem létező diák ID!")
            return
        print("\nMit szeretnél módosítani?")
        print("1. Személyes adatok")
        print("2. Szülők adatai")
        print("3. Hiányzások")
        print("4. Osztály")
        try:
            valasztas = int(input("\nVálassz opciót: "))
            if valasztas == 1:
                diak = AdatKezeles.adatok["diakok"][diak_id]
                print("\nJelenlegi adatok:")
                print(f"1. Név: {diak['nev']}")
                print(f"2. Születési dátum: {diak['szuletesi_datum']}")
                print(f"3. Lakcím: {diak['lakcim']}")
                print(f"4. Telefonszám: {diak['telefonszam']}")
                mit_modosit = int(input("\nMelyik adatot módosítanád (1-4): "))
                if mit_modosit == 1:
                    uj_nev = input("Add meg az új nevet: ")
                    diak['nev'] = uj_nev
                    diak['email'] = f"{uj_nev.lower().replace(' ', '.')}@diak.iskola.hu"
                elif mit_modosit == 2:
                    diak['szuletesi_datum'] = input("Add meg az új születési dátumot: ")
                elif mit_modosit == 3:
                    diak['lakcim'] = input("Add meg az új lakcímet: ")
                elif mit_modosit == 4:
                    diak['telefonszam'] = input("Add meg az új telefonszámot: ")
                else:
                    print("Érvénytelen választás!")
                    return
            elif valasztas == 2:
                diak = AdatKezeles.adatok["diakok"][diak_id]
                print("\nMelyik szülő adatait módosítanád?")
                print("1. Anya")
                print("2. Apa")
                szulo_valasztas = int(input("\nVálassz opciót: "))
                if szulo_valasztas == 1:
                    szulo = "anya"
                elif szulo_valasztas == 2:
                    szulo = "apa"
                    if 'apa' not in diak['szulok']:
                        print("Nincs apa rögzítve!")
                        return
                else:
                    print("Érvénytelen választás!")
                    return
                print("\nMit szeretnél módosítani?")
                print("1. Név")
                print("2. Telefonszám")
                print("3. Email")
                adat_valasztas = int(input("\nVálassz opciót: "))
                if adat_valasztas == 1:
                    diak['szulok'][szulo]['nev'] = input("Add meg az új nevet: ")
                elif adat_valasztas == 2:
                    diak['szulok'][szulo]['telefonszam'] = input("Add meg az új telefonszámot: ")
                elif adat_valasztas == 3:
                    diak['szulok'][szulo]['email'] = input("Add meg az új email címet: ")
                else:
                    print("Érvénytelen választás!")
                    return
            elif valasztas == 3:
                diak = AdatKezeles.adatok["diakok"][diak_id]
                print("\nJelenlegi hiányzások:")
                print(f"Igazolt: {diak['hianyzasok']['igazolt']}")
                print(f"Igazolatlan: {diak['hianyzasok']['igazolatlan']}")
                try:
                    diak['hianyzasok']['igazolt'] = int(input("\nAdd meg az új igazolt hiányzások számát: "))
                    diak['hianyzasok']['igazolatlan'] = int(input("Add meg az új igazolatlan hiányzások számát: "))
                except ValueError:
                    print("Érvénytelen szám!")
                    return
            elif valasztas == 4:
                diak = AdatKezeles.adatok["diakok"][diak_id]
                regi_osztaly_id = diak.get('osztaly_id')
                print("\nElérhető osztályok:")
                for osztaly_id in AdatKezeles.adatok["osztalyok"].keys():
                    print(f"- {osztaly_id}")
                uj_osztaly_id = input("\nAdd meg az új osztályt: ")
                if uj_osztaly_id not in AdatKezeles.adatok["osztalyok"]:
                    print("Nem létező osztály!")
                    return
                if regi_osztaly_id:
                    AdatKezeles.adatok["osztalyok"][regi_osztaly_id]["diak_ids"].remove(diak_id)
                    AdatKezeles.adatok["osztalyok"][regi_osztaly_id]["letszam"] -= 1
                diak['osztaly_id'] = uj_osztaly_id
                AdatKezeles.adatok["osztalyok"][uj_osztaly_id]["diak_ids"].append(diak_id)
                AdatKezeles.adatok["osztalyok"][uj_osztaly_id]["letszam"] += 1
            else:
                print("Érvénytelen választás!")
                return
            print("\nAdatok sikeresen módosítva!")
        except ValueError:
            print("Érvénytelen bemenet!")

    @staticmethod
    def diak_torlese():
        """
        Diák törlése a rendszerből. Ellenőrzi, hogy a diák törölhető-e (nincsenek jegyei),
        majd végrehajtja a törlést és frissíti az osztály létszámát.
        """
        print("\nDiák törlése")
        print("-" * 20)
        Diakok.diakok_listazasa()
        diak_id = input("\nAdd meg a törölni kívánt diák ID-jét: ")
        if diak_id not in AdatKezeles.adatok["diakok"]:
            print("Nem létező diák ID!")
            return
        for jegy in AdatKezeles.adatok["jegyek"].values():
            if jegy["diak_id"] == diak_id:
                print("A diák nem törölhető, mert vannak jegyei!")
                return
        diak = AdatKezeles.adatok["diakok"][diak_id]
        if 'osztaly_id' in diak:
            osztaly = AdatKezeles.adatok["osztalyok"][diak['osztaly_id']]
            osztaly["diak_ids"].remove(diak_id)
            osztaly["letszam"] -= 1
        del AdatKezeles.adatok["diakok"][diak_id]
        print("\nDiák sikeresen törölve!")

    @staticmethod
    def diak_keresese():
        """
        Diákok keresése különböző szempontok alapján (név, osztály, lakcím).
        Részletes információkat jelenít meg a találatokról.
        """
        print("\nDiák keresése")
        print("-" * 20)
        print("Keresési opciók:")
        print("1. Név alapján")
        print("2. Osztály alapján")
        print("3. Lakcím alapján")
        try:
            valasztas = int(input("\nVálassz keresési opciót: "))
            if valasztas == 1:
                nev = input("Add meg a keresett nevet vagy névtöredéket: ").lower()
                talalatok = []
                for diak_id, diak in AdatKezeles.adatok["diakok"].items():
                    if nev in diak["nev"].lower():
                        talalatok.append(diak_id)
            elif valasztas == 2:
                osztaly = input("Add meg az osztályt: ")
                talalatok = []
                for diak_id, diak in AdatKezeles.adatok["diakok"].items():
                    if 'osztaly_id' in diak and diak["osztaly_id"] == osztaly:
                        talalatok.append(diak_id)
            elif valasztas == 3:
                lakcim = input("Add meg a keresett lakcímet vagy címtöredéket: ").lower()
                talalatok = []
                for diak_id, diak in AdatKezeles.adatok["diakok"].items():
                    if lakcim in diak["lakcim"].lower():
                        talalatok.append(diak_id)
            else:
                print("Érvénytelen választás!")
                return
            if talalatok:
                print("\nTalálatok:")
                for diak_id in talalatok:
                    diak = AdatKezeles.adatok["diakok"][diak_id]
                    print(f"\nNév: {diak['nev']}")
                    print(f"ID: {diak_id}")
                    print(f"Osztály: {diak.get('osztaly_id', 'Nincs osztály')}")
                    print(f"Születési dátum: {diak['szuletesi_datum']}")
                    print(f"Lakcím: {diak['lakcim']}")
                    print(f"Telefonszám: {diak['telefonszam']}")
                    print(f"Email: {diak['email']}")
                    print("Hiányzások:")
                    print(f"  Igazolt: {diak['hianyzasok']['igazolt']}")
                    print(f"  Igazolatlan: {diak['hianyzasok']['igazolatlan']}")
                    print("-" * 30)
                else:
                    print("\nNincs találat a keresési feltételeknek megfelelően!")
        except ValueError:
            print("Érvénytelen bemenet!")

    @staticmethod
    def diak_menu():
        """
        A diákok kezelésére szolgáló menürendszer.

        Megjeleníti és kezeli a diákokkal kapcsolatos műveletek menüjét:
        - Új diák felvétele
        - Diák adatainak módosítása
        - Diák törlése
        - Diákok listázása
        - Diák keresése
        - Visszatérés a főmenübe
        """
        while True:
            print('----------------------------------------------')
            print('Diákok Kezelése!')
            print('1. Új Diák Felvétele.')
            print('2. Diák Adatainak Módosítása.')
            print('3. Diák Törlése.')
            print('4. Diák Listázása.')
            print('5. Diák Keresése.')
            print('6. Vissza a főmenübe')

            try:
                valasztott = int(input('Kérlek válassz a menüpontok közül: '))
                match valasztott:
                    case 1:
                        Diakok.uj_diak_felvetele()
                    case 2:
                        Diakok.diak_adatainak_modositasa()
                    case 3:
                        Diakok.diak_torlese()
                    case 4:
                        Diakok.diakok_listazasa()
                    case 5:
                        Diakok.diak_keresese()
                    case 6:
                        return
                    case _:
                        print("Érvénytelen választás!")
            except ValueError:
                print("Kérlek számot adj meg!")


class Osztalyok:
    """
    Az osztályok kezelésért felelős osztály, amely tartalmazza az osztályokkal kapcsolatos műveleteket.
    """
    @staticmethod
    def osztalyok_listazasa():
        """
        Kilistázza az összes osztály adatait, beleértve az osztályfőnököt, diákokat,
        tantárgyakat és órarendet.
        """
        for osztaly_id, osztaly_adatok in AdatKezeles.adatok["osztalyok"].items():
            print(f"\nOsztály: {osztaly_adatok['id']}")
            osztalyfonok = AdatKezeles.adatok["tanarok"][osztaly_adatok['osztalyfonok_id']]
            print(f"Osztályfőnök: {osztalyfonok['nev']}")
            print(f"Létszám: {osztaly_adatok['letszam']}")
            print("\nDiákok:")
            for diak_id in osztaly_adatok['diak_ids']:
                if diak_id in AdatKezeles.adatok["diakok"]:
                    print(f"- {AdatKezeles.adatok['diakok'][diak_id]['nev']}")
            print("\nTantárgyak és óraszámok:")
            for tantargy, adatok in osztaly_adatok['tantargyak'].items():
                tanar = AdatKezeles.adatok["tanarok"][adatok['tanar_id']]['nev']
                print(f"  {tantargy}: {adatok['heti_oraszam']} óra (Tanár: {tanar})")
            print("\nÓrarend:")
            for nap, orak in osztaly_adatok['orarend'].items():
                print(f"  {nap}: {', '.join(orak)}")
            print("-" * 50)

    @staticmethod
    def uj_osztaly_letrehozasa():
        """
        Új osztály létrehozása. Beállítja az osztályfőnököt, tantárgyakat, tanárokat
        és létrehozza az órarendet.
        """
        print("\nÚj osztály létrehozása")
        print("-" * 20)
        osztaly_id = input("Add meg az osztály azonosítóját (pl. '9.A'): ")
        if osztaly_id in AdatKezeles.adatok["osztalyok"]:
            print("Ez az osztály már létezik!")
            return
        print("\nVálassz osztályfőnököt:")
        for tanar_id, tanar in AdatKezeles.adatok["tanarok"].items():
            if 'osztalyfonok' not in tanar:
                print(f"- {tanar['nev']} (ID: {tanar_id})")

        osztalyfonok_id = input("\nAdd meg a választott osztályfőnök ID-jét: ")
        if osztalyfonok_id not in AdatKezeles.adatok["tanarok"]:
            print("Nem létező tanár ID!")
            return
        tantargyak = {}
        print("\nTantárgyak hozzáadása")
        while True:
            print("\nElérhető tantárgyak:")
            for tantargy in AdatKezeles.adatok["tantargyak"].values():
                print(f"- {tantargy['nev']}")
            tantargy_nev = input("\nAdd meg a tantárgy nevét (vagy 'vege' a befejezéshez): ").lower()
            if tantargy_nev == 'vege':
                break
            if tantargy_nev not in AdatKezeles.adatok["tantargyak"]:
                print("Nem létező tantárgy!")
                continue
            try:
                heti_oraszam = int(input("Add meg a heti óraszámot: "))
            except ValueError:
                print("Érvénytelen óraszám!")
                continue
            print("\nVálassz tanárt a tantárgyhoz:")
            alkalmas_tanarok = []
            for tanar_id, tanar in AdatKezeles.adatok["tanarok"].items():
                if "tantargyak" in tanar and tantargy_nev in tanar["tantargyak"]:
                    alkalmas_tanarok.append(tanar_id)
                    print(f"- {tanar['nev']} (ID: {tanar_id})")
            if not alkalmas_tanarok:
                print("Nincs megfelelő tanár ehhez a tantárgyhoz!")
                continue
            tanar_id = input("Add meg a választott tanár ID-jét: ")
            if tanar_id not in alkalmas_tanarok:
                print("Érvénytelen tanár választás!")
                continue
            tantargyak[tantargy_nev] = {
                "tanar_id": tanar_id,
                "heti_oraszam": heti_oraszam
            }
        napok = ["hetfo", "kedd", "szerda", "csutortok", "pentek"]
        orarend = {}
        print("\nÓrarend összeállítása")
        for nap in napok:
            print(f"\n{nap.capitalize()} óráinak megadása")
            print("Add meg a tantárgyakat sorrendben (vesszővel elválasztva):")
            orak = input().lower().split(",")
            orak = [ora.strip() for ora in orak]
            if not all(ora in tantargyak for ora in orak):
                print("Érvénytelen tantárgy az órarendben!")
                return
            orarend[nap] = orak
        uj_osztaly = {
            "id": osztaly_id,
            "osztalyfonok_id": osztalyfonok_id,
            "letszam": 0,
            "diak_ids": [],
            "tantargyak": tantargyak,
            "orarend": orarend
        }
        AdatKezeles.adatok["tanarok"][osztalyfonok_id]["osztalyfonok"] = osztaly_id
        AdatKezeles.adatok["osztalyok"][osztaly_id] = uj_osztaly
        print("\nOsztály sikeresen létrehozva!")

    @staticmethod
    def osztalyfonok_hozzarendeles():
        """
        Osztályfőnök módosítása egy osztályhoz. A régi osztályfőnök felszabadítása
        és az új hozzárendelése.
        """
        print("\nOsztályfőnök hozzárendelése")
        print("-" * 20)
        print("Válassz osztályt:")
        for osztaly_id in AdatKezeles.adatok["osztalyok"]:
            print(f"- {osztaly_id}")
        osztaly_id = input("\nAdd meg az osztály azonosítóját: ")
        if osztaly_id not in AdatKezeles.adatok["osztalyok"]:
            print("Nem létező osztály!")
            return
        print("\nVálassz új osztályfőnököt:")
        for tanar_id, tanar in AdatKezeles.adatok["tanarok"].items():
            if 'osztalyfonok' not in tanar:
                print(f"- {tanar['nev']} (ID: {tanar_id})")
        uj_osztalyfonok_id = input("\nAdd meg az új osztályfőnök ID-jét: ")
        if uj_osztalyfonok_id not in AdatKezeles.adatok["tanarok"]:
            print("Nem létező tanár ID!")
            return
        regi_osztalyfonok_id = AdatKezeles.adatok["osztalyok"][osztaly_id]["osztalyfonok_id"]
        if 'osztalyfonok' in AdatKezeles.adatok["tanarok"][regi_osztalyfonok_id]:
            del AdatKezeles.adatok["tanarok"][regi_osztalyfonok_id]["osztalyfonok"]
        AdatKezeles.adatok["osztalyok"][osztaly_id]["osztalyfonok_id"] = uj_osztalyfonok_id
        AdatKezeles.adatok["tanarok"][uj_osztalyfonok_id]["osztalyfonok"] = osztaly_id
        print("\nOsztályfőnök sikeresen módosítva!")

    @staticmethod
    def diak_hozzaadasa_osztalyhoz():
        """
        Diák hozzáadása egy osztályhoz. Frissíti az osztály létszámát és a diák adatait.
        """
        print("\nDiák hozzáadása osztályhoz")
        print("-" * 20)
        print("Válassz osztályt:")
        for osztaly_id in AdatKezeles.adatok["osztalyok"]:
            print(f"- {osztaly_id}")
        osztaly_id = input("\nAdd meg az osztály azonosítóját: ")
        if osztaly_id not in AdatKezeles.adatok["osztalyok"]:
            print("Nem létező osztály!")
            return
        print("\nVálassz diákot:")
        van_elerheto_diak = False
        for diak_id, diak in AdatKezeles.adatok["diakok"].items():
            if 'osztaly_id' not in diak or not diak['osztaly_id']:
                van_elerheto_diak = True
                print(f"- {diak['nev']} (ID: {diak_id})")
        if not van_elerheto_diak:
            print("Nincs elérhető diák!")
            return
        diak_id = input("\nAdd meg a diák ID-jét: ")
        if diak_id not in AdatKezeles.adatok["diakok"]:
            print("Nem létező diák ID!")
            return
        AdatKezeles.adatok["diakok"][diak_id]["osztaly_id"] = osztaly_id
        AdatKezeles.adatok["osztalyok"][osztaly_id]["diak_ids"].append(diak_id)
        AdatKezeles.adatok["osztalyok"][osztaly_id]["letszam"] += 1
        print("\nDiák sikeresen hozzáadva az osztályhoz!")

    @staticmethod
    def osztaly_adatainak_modositasa():
        """
        Osztály adatainak módosítása, beleértve tantárgyak óraszámát, órarendet
        és tantárgyak tanárait.
        """
        print("\nOsztály adatainak módosítása")
        print("-" * 20)
        print("Válassz osztályt:")
        for osztaly_id in AdatKezeles.adatok["osztalyok"]:
            print(f"- {osztaly_id}")
        osztaly_id = input("\nAdd meg az osztály azonosítóját: ")
        if osztaly_id not in AdatKezeles.adatok["osztalyok"]:
            print("Nem létező osztály!")
            return
        print("\nMit szeretnél módosítani?")
        print("1. Tantárgy óraszámának módosítása")
        print("2. Órarend módosítása")
        print("3. Tantárgy tanárának módosítása")
        try:
            valasztas = int(input("\nVálassz opciót: "))
            if valasztas == 1:
                print("\nVálassz tantárgyat:")
                for tantargy in AdatKezeles.adatok["osztalyok"][osztaly_id]["tantargyak"]:
                    print(f"- {tantargy}")
                tantargy = input("\nAdd meg a tantárgy nevét: ").lower()
                if tantargy not in AdatKezeles.adatok["osztalyok"][osztaly_id]["tantargyak"]:
                    print("Nem létező tantárgy!")
                    return
                try:
                    uj_oraszam = int(input("Add meg az új heti óraszámot: "))
                    AdatKezeles.adatok["osztalyok"][osztaly_id]["tantargyak"][tantargy]["heti_oraszam"] = uj_oraszam
                    print("\nÓraszám sikeresen módosítva!")
                except ValueError:
                    print("Érvénytelen óraszám!")
            elif valasztas == 2:
                napok = ["hetfo", "kedd", "szerda", "csutortok", "pentek"]
                print("\nVálassz napot:")
                for nap in napok:
                    print(f"- {nap}")
                nap = input("\nAdd meg a napot: ").lower()
                if nap not in napok:
                    print("Érvénytelen nap!")
                    return
                print("\nJelenlegi órák ezen a napon:",
                      ", ".join(AdatKezeles.adatok["osztalyok"][osztaly_id]["orarend"][nap]))
                print("Add meg az új órarendet (tantárgyak vesszővel elválasztva):")
                uj_orak = input().lower().split(",")
                uj_orak = [ora.strip() for ora in uj_orak]
                if not all(ora in AdatKezeles.adatok["osztalyok"][osztaly_id]["tantargyak"] for ora in uj_orak):
                    print("Érvénytelen tantárgy az órarendben!")
                    return
                AdatKezeles.adatok["osztalyok"][osztaly_id]["orarend"][nap] = uj_orak
                print("\nÓrarend sikeresen módosítva!")
            elif valasztas == 3:
                print("\nVálassz tantárgyat:")
                for tantargy in AdatKezeles.adatok["osztalyok"][osztaly_id]["tantargyak"]:
                    print(f"- {tantargy}")
                tantargy = input("\nAdd meg a tantárgy nevét: ").lower()
                if tantargy not in AdatKezeles.adatok["osztalyok"][osztaly_id]["tantargyak"]:
                    print("Nem létező tantárgy!")
                    return
                print("\nVálassz új tanárt:")
                alkalmas_tanarok = []
                for tanar_id, tanar in AdatKezeles.adatok["tanarok"].items():
                    if "tantargyak" in tanar and tantargy in tanar["tantargyak"]:
                        alkalmas_tanarok.append(tanar_id)
                        print(f"- {tanar['nev']} (ID: {tanar_id})")
                if not alkalmas_tanarok:
                    print("Nincs megfelelő tanár ehhez a tantárgyhoz!")
                    return
                uj_tanar_id = input("\nAdd meg az új tanár ID-jét: ")
                if uj_tanar_id not in alkalmas_tanarok:
                    print("Érvénytelen tanár választás!")
                    return
                AdatKezeles.adatok["osztalyok"][osztaly_id]["tantargyak"][tantargy]["tanar_id"] = uj_tanar_id
                print("\nTanár sikeresen módosítva!")
            else:
                print("Érvénytelen választás!")
        except ValueError:
            print("Érvénytelen bemenet!")

    @staticmethod
    def osztalyok_menu():
        """
        Az osztályok kezelésére szolgáló menürendszer.

        Megjeleníti és kezeli az osztályokkal kapcsolatos műveletek menüjét:
        - Új osztály létrehozása
        - Osztályfőnök hozzárendelés
        - Diák hozzáadása osztályhoz
        - Osztályok listázása
        - Osztály adatainak módosítása
        - Visszatérés a főmenübe
        """
        while True:
            print('----------------------------------------------')
            print('Osztályok Kezelése!')
            print('1. Új Osztály Létrehozása.')
            print('2. Osztályfőnök Hozzárendelés.')
            print('3. Diák Hozzáadása Osztályhoz.')
            print('4. Osztályok Listázása.')
            print('5. Osztály Adatainak Módosítása.')
            print('6. Vissza a főmenübe')

            try:
                valasztott = int(input('Kérlek válassz a menüpontok közül: '))
                match valasztott:
                    case 1:
                        Osztalyok.uj_osztaly_letrehozasa()
                    case 2:
                        Osztalyok.osztalyfonok_hozzarendeles()
                    case 3:
                        Osztalyok.diak_hozzaadasa_osztalyhoz()
                    case 4:
                        Osztalyok.osztalyok_listazasa()
                    case 5:
                        Osztalyok.osztaly_adatainak_modositasa()
                    case 6:
                        return
                    case _:
                        print("Érvénytelen választás!")
            except ValueError:
                print("Kérlek számot adj meg!")


class Tantargyak:
    """
    A tantárgyak kezelésért felelős osztály, amely tartalmazza a tantárgyakkal kapcsolatos műveleteket.
    """
    @staticmethod
    def tantargyak_listazasa():
        """
        Kilistázza az összes tantárgy adatait, beleértve az óraszámokat, évfolyamokat
        és tematikát.
        """
        for tantargy_id, tantargy_adatok in AdatKezeles.adatok["tantargyak"].items():
            print(f"Tantárgy: {tantargy_adatok['nev']}")
            print(f"ID: {tantargy_adatok['id']}")
            print(f"Óraszám: {tantargy_adatok['alap_heti_oraszam']}")
            print(f"Évfolyamok: {tantargy_adatok['evfolyamok']}")
            print(f"Követelmény: {tantargy_adatok['kovetelmeny']}")
            print(f"Leírás: {tantargy_adatok['leiras']}")
            print("\nTematika:")
            for evfolyam, temak in tantargy_adatok['tematika'].items():
                print(f"{evfolyam}. évfolyam: {', '.join(temak)}")
            print("-" * 50)

    @staticmethod
    def uj_tantargy_felvetele():
        """
        Új tantárgy felvétele a rendszerbe. Beállítja az alapadatokat, évfolyamokat
        és részletes tematikát.
        """
        print("\nÚj tantárgy felvétele")
        print("-" * 20)

        uj_id = f"M{len(AdatKezeles.adatok['tantargyak']) + 1:03d}"
        nev = input("Add meg a tantárgy nevét: ").lower()
        try:
            oraszam = int(input("Add meg az alap heti óraszámot: "))
        except ValueError:
            print("Érvénytelen óraszám!")
            return
        print("\nAdd meg az évfolyamokat (9-12, vesszővel elválasztva)")
        evfolyamok_str = input("Évfolyamok: ")
        try:
            evfolyamok = [int(x.strip()) for x in evfolyamok_str.split(",")]
            if not all(9 <= x <= 12 for x in evfolyamok):
                raise ValueError
        except ValueError:
            print("Érvénytelen évfolyamok!")
            return
        kovetelmeny = input("Add meg a követelményszintet (közép/emelt): ")
        leiras = input("Add meg a tantárgy leírását: ")
        tematika = {}
        for evfolyam in evfolyamok:
            print(f"\n{evfolyam}. évfolyam témakörei")
            print("Add meg a témaköröket vesszővel elválasztva:")
            temakorok = input().split(",")
            temakorok = [tema.strip() for tema in temakorok]
            tematika[str(evfolyam)] = temakorok
        uj_tantargy = {
            "id": uj_id,
            "nev": nev,
            "alap_heti_oraszam": oraszam,
            "evfolyamok": evfolyamok,
            "kovetelmeny": kovetelmeny,
            "leiras": leiras,
            "tematika": tematika
        }
        AdatKezeles.adatok["tantargyak"][nev] = uj_tantargy
        print("\nTantárgy sikeresen felvéve!")

    @staticmethod
    def tantargy_hozzarendelese_tanarhoz():
        """
        Tantárgy hozzárendelése egy tanárhoz. Ellenőrzi a duplikációkat és frissíti
        a tanár tantárgylistáját.
        """
        print("\nElérhető tantárgyak:")
        for tantargy in AdatKezeles.adatok["tantargyak"].values():
            print(f"- {tantargy['nev']}")
        print("\nElérhető tanárok:")
        for tanar in AdatKezeles.adatok["tanarok"].values():
            print(f"- {tanar['nev']} (ID: {tanar['id']})")
        tanar_id = input("\nAdd meg a tanár ID-jét: ")
        if tanar_id not in AdatKezeles.adatok["tanarok"]:
            print("Nem létező tanár ID!")
            return
        tantargy_nev = input("Add meg a tantárgy nevét: ").lower()
        if tantargy_nev not in AdatKezeles.adatok["tantargyak"]:
            print("Nem létező tantárgy!")
            return
        if "tantargyak" not in AdatKezeles.adatok["tanarok"][tanar_id]:
            AdatKezeles.adatok["tanarok"][tanar_id]["tantargyak"] = []
        if tantargy_nev not in AdatKezeles.adatok["tanarok"][tanar_id]["tantargyak"]:
            AdatKezeles.adatok["tanarok"][tanar_id]["tantargyak"].append(tantargy_nev)
            print("\nTantárgy sikeresen hozzárendelve a tanárhoz!")
        else:
            print("\nEz a tantárgy már hozzá van rendelve ehhez a tanárhoz!")

    @staticmethod
    def tantargy_torlese():
        """
        Tantárgy törlése a rendszerből. Ellenőrzi, hogy a tantárgy törölhető-e
        (nincs aktív osztályban és nincsenek hozzá jegyek).
        """
        print("\nElérhető tantárgyak:")
        for tantargy in AdatKezeles.adatok["tantargyak"].values():
            print(f"- {tantargy['nev']}")
        tantargy_nev = input("\nAdd meg a törölni kívánt tantárgy nevét: ").lower()
        if tantargy_nev not in AdatKezeles.adatok["tantargyak"]:
            print("Nem létező tantárgy!")
            return
        tantargy_id = AdatKezeles.adatok["tantargyak"][tantargy_nev]["id"]
        for osztaly in AdatKezeles.adatok["osztalyok"].values():
            if tantargy_nev in osztaly["tantargyak"]:
                print("A tantárgy nem törölhető, mert aktív osztályokban szerepel!")
                return
        for jegy in AdatKezeles.adatok["jegyek"].values():
            if jegy["tantargy_id"] == tantargy_id:
                print("A tantárgy nem törölhető, mert vannak hozzá tartozó jegyek!")
                return
        for tanar in AdatKezeles.adatok["tanarok"].values():
            if "tantargyak" in tanar and tantargy_nev in tanar["tantargyak"]:
                tanar["tantargyak"].remove(tantargy_nev)
        del AdatKezeles.adatok["tantargyak"][tantargy_nev]
        print("\nTantárgy sikeresen törölve!")

    @staticmethod
    def tantargyak_menu():
        """
        A tantárgyak kezelésére szolgáló menürendszer.

        Megjeleníti és kezeli a tantárgyakkal kapcsolatos műveletek menüjét:
        - Új tantárgy felvétele
        - Tantárgy hozzárendelése tanárhoz
        - Tantárgyak listázása
        - Tantárgy törlése
        - Visszatérés a főmenübe
        """
        while True:
            print('----------------------------------------------')
            print('Tantárgy kezelés!')
            print('1. Új Tantárgy Felvétele.')
            print('2. Tantárgy hozzárendelése tanárhoz.')
            print('3. Tantárgyak Listázása.')
            print('4. Tantárgy Törlése.')
            print('5. Vissza a főmenübe')

            try:
                valasztott = int(input('Kérlek válassz a menüpontok közül: '))
                match valasztott:
                    case 1:
                        Tantargyak.uj_tantargy_felvetele()
                    case 2:
                        Tantargyak.tantargy_hozzarendelese_tanarhoz()
                    case 3:
                        Tantargyak.tantargyak_listazasa()
                    case 4:
                        Tantargyak.tantargy_torlese()
                    case 5:
                        return
                    case _:
                        print("Érvénytelen választás!")
            except ValueError:
                print("Kérlek számot adj meg!")


class Jegyek:
    """
    A jegyek kezelésért felelős osztály, amely tartalmazza az osztályzatokkal kapcsolatos műveleteket.
    """
    @staticmethod
    def jegyek_listazasa():
        """
        Az összes jegy listázása részletes információkkal.
        """
        for jegy_id, jegy_adatok in AdatKezeles.adatok["jegyek"].items():
            print(f"Diák ID: {jegy_adatok['diak_id']}")
            print(f"Tantárgy ID: {jegy_adatok['tantargy_id']}")
            print(f"Érték: {jegy_adatok['ertek']}")
            print(f"Dátum: {jegy_adatok['datum']}")
            print(f"Típus: {jegy_adatok['tipus']}")
            print(f"Téma: {jegy_adatok['tema']}")
            if 'megjegyzes' in jegy_adatok:
                print(f"Megjegyzés: {jegy_adatok['megjegyzes']}")
            print("-" * 30)

    @staticmethod
    def list_diakok():
        """
         Az összes diák nevének listázása.

         Segédfunkció a diákok kiválasztásához más műveletek során.
         """
        print("\nElérhető diákok:")
        print("-" * 20)
        for diak in AdatKezeles.adatok["diakok"].values():
            print(f"- {diak['nev']}")

    @staticmethod
    def jegyek_listazasa_diak_szerint():
        """
        Egy adott diák jegyeinek listázása tantárgyak szerint.
        """
        Jegyek.list_diakok()
        nev = input("\nAdd meg a diák nevét: ")
        volt_talalat = False
        for diak_id, diak in AdatKezeles.adatok["diakok"].items():
            if nev.lower() in diak['nev'].lower():
                volt_talalat = True
                print(f"\nDiák: {diak['nev']}")
                print("-" * 20)
                for jegy_id, jegy in AdatKezeles.adatok["jegyek"].items():
                    if jegy['diak_id'] == diak_id:
                        print(f"Tantárgy: {Azonosito.get_tantargy_nev(jegy['tantargy_id'])}")
                        print(f"Érték: {jegy['ertek']}")
                        print(f"Dátum: {jegy['datum']}")
                        print(f"Típus: {jegy['tipus']}")
                        print("-" * 15)

        if not volt_talalat:
            print("Nincs ilyen nevű diák!")

    @staticmethod
    def list_tantargyak():
        """
        Az összes tantárgy nevének listázása.

        Segédfunkció a tantárgyak kiválasztásához más műveletek során.
        """
        print("\nElérhető tantárgyak:")
        print("-" * 20)
        for tantargy in AdatKezeles.adatok["tantargyak"].values():
            print(f"- {tantargy['nev']}")

    @staticmethod
    def jegyek_listazasa_tantargy_szerint():
        """
        Egy adott tantárgy jegyeinek listázása diákok szerint.
        """
        Jegyek.list_tantargyak()
        tantargy = input("\nAdd meg a tantárgy nevét: ")
        volt_talalat = False
        for jegy_id, jegy in AdatKezeles.adatok["jegyek"].items():
            if tantargy.lower() in Azonosito.get_tantargy_nev(jegy['tantargy_id']).lower():
                diak = AdatKezeles.adatok["diakok"][jegy['diak_id']]
                if not volt_talalat:
                    print(f"\nTantárgy: {tantargy}")
                    print("-" * 20)
                volt_talalat = True
                print(f"Diák: {diak['nev']}")
                print(f"Érték: {jegy['ertek']}")
                print(f"Dátum: {jegy['datum']}")
                print(f"Típus: {jegy['tipus']}")
                print("-" * 15)

        if not volt_talalat:
            print("Nincs ilyen tantárgyból jegy!")

    @staticmethod
    def atlagok_szamitasa():
        """
        Különböző típusú átlagok számítása (diák, osztály, tantárgy szerint).
        """
        print("\nÁtlagszámítás típusai:")
        print("1. Diák átlaga tantárgyanként")
        print("2. Osztály átlaga tantárgyanként")
        print("3. Tantárgy átlaga")

        valasztas = int(input("\nVálassz egy opciót: "))
        match valasztas:
            case 1:
                Jegyek.diak_atlag()
            case 2:
                Jegyek.osztaly_atlag()
            case 3:
                Jegyek.tantargy_atlag()

    @staticmethod
    def diak_atlag():
        def diak_atlag():
            """
            Egy diák tantárgyankénti átlagának kiszámítása.

            Kilistázza az elérhető diákokat, bekéri a diák nevét, majd kiszámítja és megjeleníti
            az átlagait minden tantárgyból. A számítás csak az érvényes jegyeket veszi figyelembe.
            """
        Jegyek.list_diakok()
        nev = input("\nAdd meg a diák nevét: ").lower()

        def get_diak():
            """
            Diák azonosítójának és adatainak lekérdezése név alapján.

            Returns:
                tuple: (diak_id, diak_adatok) pár, ahol a diak_id a diák azonosítója,
                      a diak_adatok pedig a diák összes adata

            Raises:
                StopIteration: Ha nem található a keresett nevű diák
            """
            return next(
                (diak_id, diak) for diak_id, diak in AdatKezeles.adatok["diakok"].items()
                if nev in diak['nev'].lower()
            )

        def get_jegyek(diak_id):
            """
            Egy diák összes jegyének lekérdezése tantárgyak szerint csoportosítva.

            Args:
                diak_id (str): A diák egyedi azonosítója

            Returns:
                dict: Tantárgyak szerinti jegycsoportosítás, ahol a kulcs a tantárgy neve,
                     az érték pedig a jegyek listája
            """
            jegyek = {}
            for jegy in AdatKezeles.adatok["jegyek"].values():
                if jegy['diak_id'] != diak_id:
                    continue

                tantargy = Azonosito.get_tantargy_nev(jegy['tantargy_id'])
                if tantargy not in jegyek:
                    jegyek[tantargy] = []
                jegyek[tantargy].append(jegy['ertek'])
            return jegyek

        def print_atlagok(diak_nev, jegyek):
            """
            Egy diák tantárgyankénti átlagainak kiírása.

            Args:
                diak_nev (str): A diák neve
                jegyek (dict): Tantárgyak szerinti jegycsoportosítás
            """
            print(f"\n{diak_nev} átlagai:")
            for tantargy, ertekek in jegyek.items():
                atlag = sum(ertekek) / len(ertekek)
                print(f"{tantargy}: {atlag:.2f}")

        try:
            diak_id, diak = get_diak()
            jegyek = get_jegyek(diak_id)
            print_atlagok(diak['nev'], jegyek)
        except StopIteration:
            print("Nem található ilyen nevű diák.")

    @staticmethod
    def osztaly_atlag():
        """
        Egy osztály tantárgyankénti átlagának kiszámítása.

        Minden osztályra és azon belül minden tantárgyra kiszámítja az átlagot.
        Az átlagszámítás figyelembe veszi az osztály összes diákjának jegyeit.
        """
        def get_jegyek_by_tantargy(osztaly_id, tantargy):
            """
            Egy osztály egy tantárgyból szerzett összes jegyének lekérdezése.

            Args:
                osztaly_id (str): Az osztály azonosítója
                tantargy (str): A tantárgy neve

            Returns:
                list: A megadott tantárgyból szerzett jegyek listája
            """
            jegyek = []
            for diak_id in AdatKezeles.adatok["osztalyok"][osztaly_id]["diak_ids"]:
                jegyek.extend(
                    jegy["ertek"]
                    for jegy in AdatKezeles.adatok["jegyek"].values()
                    if (jegy["diak_id"] == diak_id and
                        Azonosito.get_tantargy_nev(jegy["tantargy_id"]) == tantargy)
                )
            return jegyek

        def calculate_print_atlag(tantargy, jegyek):
            """
            Átlag számítása és kiírása egy tantárgy jegyeiből.

            Args:
                tantargy (str): A tantárgy neve
                jegyek (list): A tantárgyhoz tartozó jegyek listája
            """
            if jegyek:
                atlag = sum(jegyek) / len(jegyek)
                print(f"{tantargy}: {atlag:.2f}")

        for osztaly_id, osztaly in AdatKezeles.adatok["osztalyok"].items():
            print(f"\n{osztaly_id} osztály átlagai:")
            for tantargy in osztaly["tantargyak"]:
                jegyek = get_jegyek_by_tantargy(osztaly_id, tantargy)
                calculate_print_atlag(tantargy, jegyek)

    @staticmethod
    def tantargy_atlag():
        """
        Egy tantárgy átlagának kiszámítása az összes diák jegyei alapján.

        Kilistázza az elérhető tantárgyakat, bekéri a választott tantárgy nevét,
        majd kiszámítja az átlagot az összes beírt jegy alapján.
        """
        Jegyek.list_tantargyak()
        tantargy = input("\nAdd meg a tantárgy nevét: ")
        jegyek = []
        for jegy in AdatKezeles.adatok["jegyek"].values():
            if tantargy.lower() in Azonosito.get_tantargy_nev(jegy['tantargy_id']).lower():
                jegyek.append(jegy['ertek'])
        if jegyek:
            atlag = sum(jegyek) / len(jegyek)
            print(f"\n{tantargy} átlaga: {atlag:.2f}")
        else:
            print("Nincs ilyen tantárgy vagy nincs hozzá jegy!")

    @staticmethod
    def jegy_beirasa():
        """
        Új jegy beírása egy diáknak egy adott tantárgyból. Ellenőrzi a jogosultságokat
        és a jegy érvényességét.
        """
        Jegyek.list_diakok()
        diak_nev = input("\nAdd meg a diák nevét: ")

        diak_id = None
        for d_id, diak in AdatKezeles.adatok["diakok"].items():
            if diak_nev.lower() in diak['nev'].lower():
                diak_id = d_id
                print(f"\nKiválasztott diák: {diak['nev']}")
                break
        if not diak_id:
            print("Nincs ilyen diák!")
            return
        diak_osztaly = AdatKezeles.adatok["diakok"][diak_id]["osztaly_id"]
        print("\nVálasztható tantárgyak:")
        for tantargy, adatok in AdatKezeles.adatok["osztalyok"][diak_osztaly]["tantargyak"].items():
            tanar = AdatKezeles.adatok["tanarok"][adatok["tanar_id"]]["nev"]
            print(f"- {tantargy} (Tanár: {tanar})")
        tantargy = input("\nAdd meg a tantárgy nevét: ")
        tantargy_id = None
        for t_adat in AdatKezeles.adatok["tantargyak"].values():
            if tantargy.lower() == t_adat['nev'].lower():
                tantargy_id = t_adat['id']
                break
        if not tantargy_id:
            print("Nincs ilyen tantárgy!")
            return
        try:
            ertek = int(input("Add meg a jegyet (1-5): "))
            if ertek not in range(1, 6):
                print("Érvénytelen jegy!")
                return
        except ValueError:
            print("Érvénytelen érték!")
            return

        datum = input("Add meg a dátumot (ÉÉÉÉ-HH-NN): ")
        print("\nLehetséges típusok: dolgozat, felelet, gyakorlati, projektmunka")
        tipus = input("Add meg a típust: ")
        tema = input("Add meg a témát: ")
        megjegyzes = input("Megjegyzés (opcionális): ")
        tanar_id = AdatKezeles.adatok["osztalyok"][diak_osztaly]["tantargyak"][tantargy]["tanar_id"]
        uj_id = f"J{len(AdatKezeles.adatok['jegyek']) + 1:03d}"
        uj_jegy = {
            "id": uj_id,
            "diak_id": diak_id,
            "tantargy_id": tantargy_id,
            "ertek": ertek,
            "datum": datum,
            "tipus": tipus,
            "tanar_id": tanar_id,
            "tema": tema
        }
        if megjegyzes:
            uj_jegy["megjegyzes"] = megjegyzes
        AdatKezeles.adatok["jegyek"][uj_id] = uj_jegy
        print("\nJegy sikeresen beírva!")

    @staticmethod
    def jegyek_menu():
        """
        A jegyek kezelésére szolgáló menürendszer.

        Megjeleníti és kezeli a jegyekkel kapcsolatos műveletek menüjét:
        - Jegyek beírása
        - Jegyek listázása diákonként
        - Jegyek listázása tantárgyanként
        - Átlagok számítása
        - Összes jegy listázása
        - Visszatérés a főmenübe
        """
        while True:
            print('----------------------------------------------')
            print('Jegy kezelés!')
            print('1. Jegyek Beírása.')
            print('2. Jegyek Listázása Diákonként.')
            print('3. Jegyek Listázása Tantárgyanként.')
            print('4. Átlagok Számítása.')
            print('5. Összes Jegyek Listázása')
            print('6. Vissza a főmenübe')
            try:
                valasztott = int(input('Kérlek válassz a menüpontok közül: '))
                match valasztott:
                    case 1:
                        Jegyek.jegy_beirasa()
                    case 2:
                        Jegyek.jegyek_listazasa_diak_szerint()
                    case 3:
                        Jegyek.jegyek_listazasa_tantargy_szerint()
                    case 4:
                        Jegyek.atlagok_szamitasa()
                    case 5:
                        Jegyek.jegyek_listazasa()
                    case 6:
                        return
                    case _:
                        print("Érvénytelen választás!")
            except ValueError:
                print("Kérlek számot adj meg!")


while True:
    print('\nOsztály Napló Rendszer!')
    Tanev.tanev()
    print('1. Tanárok Kezelése.')
    print('2. Diákok kezelése.')
    print('3. Osztályok kezelése.')
    print('4. Tantárgyak kezelése.')
    print('5. Jegyek kezelése.')
    print('6. Kilépés')

    try:
        valasztott = int(input('Kérlek válassz a menüpontok közül: '))
        match valasztott:
            case 1:
                Tanarok.tanar_menu()
            case 2:
                Diakok.diak_menu()
            case 3:
                Osztalyok.osztalyok_menu()
            case 4:
                Tantargyak.tantargyak_menu()
            case 5:
                Jegyek.jegyek_menu()
            case 6:
                print("Viszlát!")
                break
            case _:
                print("Érvénytelen választás!")
    except ValueError:
        print("Kérlek számot adj meg!")
