import json


class AdatKezeles:
    adatok = {}
    ADATBAZIS_FAJL = "iskola_adatbazis.json"

    @staticmethod
    def adatok_betoltese():
        with open(AdatKezeles.ADATBAZIS_FAJL, "r", encoding="utf-8") as f:
            AdatKezeles.adatok = json.load(f)


AdatKezeles.adatok_betoltese()


class Tanev:
    @staticmethod
    def tanev():
        return print(
            f"Üdvözöllek a {AdatKezeles.adatok['metadata']['tanev']} tanév rendszerében, "
            f"utoljára frissítve: {AdatKezeles.adatok['metadata']['utolso_frissites']}")


class Azonosito:
    @staticmethod
    def get_diak_nev(diak_id):
        return AdatKezeles.adatok['diakok'][diak_id]['nev']

    @staticmethod
    def get_tantargy_nev(tantargy_id):
        for tantargy_kulcs, tantargy_adat in AdatKezeles.adatok['tantargyak'].items():
            if tantargy_adat['id'] == tantargy_id:
                return tantargy_adat['nev']
        return tantargy_id


class Tanarok:
    @staticmethod
    def tanarok_listazasa():
        for tanar_id, tanar_adatok in AdatKezeles.adatok["tanarok"].items():
            print(f"Név: {tanar_adatok['nev']}")
            print(f"Tantárgyak: {', '.join(tanar_adatok['tantargyak'])}")
            if 'tanitott_osztalyok' in tanar_adatok:
                print(f"Tanított osztályok: {', '.join(tanar_adatok['tanitott_osztalyok'])}")
            print(f"Végzettség: {tanar_adatok['vegzettseg']}")
            print("-" * 20)

    @staticmethod
    def tanar_menu():
        print('----------------------------------------------')
        print('Tanárok Kezelése!')
        print('1. Új Tanár Felvétele.')
        print('2. Tanár Törlése.')
        print('3. Tanár Listázása.')
        print('4. Tanár Keresése.')
        print('5. Vissza a főmenübe')

        valasztott = int(input('Kérlek válassz a menüpontok közül: '))
        match valasztott:
            case 1:
                Tanarok.tanarok_listazasa()
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                return


class Diakok:
    @staticmethod
    def diakok_listazasa():
        for diak_id, diak_adatok in AdatKezeles.adatok["diakok"].items():
            print(f"Név: {diak_adatok['nev']}")
            print(f"Osztály: {diak_adatok['osztaly_id']}")
            print(f"Születési dátum: {diak_adatok['szuletesi_datum']}")
            print(f"Lakcím: {diak_adatok['lakcim']}")
            print("Szülők:")
            print(f"Anya: {diak_adatok['szulok']['anya']['nev']}")
            print(f"Tel: {diak_adatok['szulok']['anya']['telefonszam']}")
            if 'apa' in diak_adatok['szulok']:
                print(f"Apa: {diak_adatok['szulok']['apa']['nev']}")
                print(f"Tel: {diak_adatok['szulok']['apa']['telefonszam']}")
            print(f"Hiányzások:")
            print(f"Igazolt: {diak_adatok['hianyzasok']['igazolt']}")
            print(f"Igazolatlan: {diak_adatok['hianyzasok']['igazolatlan']}")
            print("-" * 20)

    @staticmethod
    def diak_menu():
        print('----------------------------------------------')
        print('Diákok Kezelése!')
        print('1. Új Diák Felvétele.')
        print('2. Diák Adatainak Módosítása.')
        print('3. Diák Törlése.')
        print('4. Diák Listázása.')
        print('5. Diák Keresése.')
        print('6. Vissza a főmenübe')

        valasztott = int(input('Kérlek válassz a menüpontok közül: '))
        match valasztott:
            case 1:
                Diakok.diakok_listazasa()
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                return


class Osztalyok:
    @staticmethod
    def osztalyok_listazasa():
        for osztaly_id, osztaly_adatok in AdatKezeles.adatok["osztalyok"].items():
            print(f"Osztály: {osztaly_adatok['id']}")
            print(f"Osztályfőnök ID: {osztaly_adatok['osztalyfonok_id']}")
            print(f"Létszám: {osztaly_adatok['letszam']}")
            print("\nTantárgyak és óraszámok:")
            for tantargy, adatok in osztaly_adatok['tantargyak'].items():
                print(f"  {tantargy}: {adatok['heti_oraszam']} óra (Tanár ID: {adatok['tanar_id']})")
            print("\nÓrarend:")
            for nap, orak in osztaly_adatok['orarend'].items():
                print(f"  {nap}: {', '.join(orak)}")
            print("-" * 50)

    @staticmethod
    def osztalyok_menu():
        print('----------------------------------------------')
        print('Osztályok Kezelése!')
        print('1. Új Osztály Létrehozása.')
        print('2. Osztályfőnök Hozzárendelés.')
        print('3. Diák Hozzáadása Osztályhoz.')
        print('4. Osztályok Listázása.')
        print('5. Osztály Adatainak Módosítása.')
        print('6. Vissza a főmenübe')

        valasztott = int(input('Kérlek válassz a menüpontok közül: '))
        match valasztott:
            case 1:
                Osztalyok.osztalyok_listazasa()
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                pass
            case 6:
                return


class Tantargyak:
    @staticmethod
    def tantargyak_listazasa():
        for tantargy_id, tantargy_adatok in AdatKezeles.adatok["tantargyak"].items():
            print(f"Tantárgy: {tantargy_adatok['nev']}")
            print(f"Óraszám: {tantargy_adatok['alap_heti_oraszam']}")
            print(f"Évfolyamok: {tantargy_adatok['evfolyamok']}")
            print("-" * 20)

    @staticmethod
    def tantargyak_menu():
        print('----------------------------------------------')
        print('Tantárgy kezelés!')
        print('1. Új Tantárgy Felvétele.')
        print('2. Tantárgy hozzárendelése tanárhoz.')
        print('3. Tantárgyak Listázása.')
        print('4. Tantárgy Törlése.')
        print('5. Vissza a főmenübe')

        valasztott = int(input('Kérlek válassz a menüpontok közül: '))
        match valasztott:
            case 1:
                Tantargyak.tantargyak_listazasa()
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case 5:
                return


class Jegyek:

    @staticmethod
    def jegyek_listazasa():
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
        print("\nElérhető diákok:")
        print("-" * 20)
        for diak in AdatKezeles.adatok["diakok"].values():
            print(f"- {diak['nev']}")

    @staticmethod
    def jegyek_listazasa_diak_szerint():
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
        print("\nElérhető tantárgyak:")
        print("-" * 20)
        for tantargy in AdatKezeles.adatok["tantargyak"].values():
            print(f"- {tantargy['nev']}")

    @staticmethod
    def jegyek_listazasa_tantargy_szerint():
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
        Jegyek.list_diakok()
        nev = input("\nAdd meg a diák nevét: ")
        for diak_id, diak in AdatKezeles.adatok["diakok"].items():
            if nev.lower() in diak['nev'].lower():
                jegyek_tantargyankent = {}
                for jegy in AdatKezeles.adatok["jegyek"].values():
                    if jegy['diak_id'] == diak_id:
                        tantargy = Azonosito.get_tantargy_nev(jegy['tantargy_id'])
                        if tantargy not in jegyek_tantargyankent:
                            jegyek_tantargyankent[tantargy] = []
                        jegyek_tantargyankent[tantargy].append(jegy['ertek'])

                print(f"\n{diak['nev']} átlagai:")
                for tantargy, jegyek in jegyek_tantargyankent.items():
                    atlag = sum(jegyek) / len(jegyek)
                    print(f"{tantargy}: {atlag:.2f}")

    @staticmethod
    def osztaly_atlag():
        for osztaly_id, osztaly in AdatKezeles.adatok["osztalyok"].items():
            print(f"\n{osztaly_id} osztály átlagai:")
            for tantargy in osztaly['tantargyak']:
                jegyek = []
                for diak_id in osztaly['diak_ids']:
                    for jegy in AdatKezeles.adatok["jegyek"].values():
                        if jegy['diak_id'] == diak_id and Azonosito.get_tantargy_nev(jegy['tantargy_id']) == tantargy:
                            jegyek.append(jegy['ertek'])
                if jegyek:
                    atlag = sum(jegyek) / len(jegyek)
                    print(f"{tantargy}: {atlag:.2f}")

    @staticmethod
    def tantargy_atlag():
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
        # Diák kiválasztása
        Jegyek.list_diakok()
        diak_nev = input("\nAdd meg a diák nevét: ")

        # Diák ID keresése
        diak_id = None
        for d_id, diak in AdatKezeles.adatok["diakok"].items():
            if diak_nev.lower() in diak['nev'].lower():
                diak_id = d_id
                print(f"\nKiválasztott diák: {diak['nev']}")
                break

        if not diak_id:
            print("Nincs ilyen diák!")
            return

        # Tantárgy kiválasztása az osztály tantárgyai közül
        diak_osztaly = AdatKezeles.adatok["diakok"][diak_id]["osztaly_id"]
        print("\nVálasztható tantárgyak:")
        for tantargy, adatok in AdatKezeles.adatok["osztalyok"][diak_osztaly]["tantargyak"].items():
            tanar = AdatKezeles.adatok["tanarok"][adatok["tanar_id"]]["nev"]
            print(f"- {tantargy} (Tanár: {tanar})")

        tantargy = input("\nAdd meg a tantárgy nevét: ")

        # Tantárgy ID keresése
        tantargy_id = None
        for t_adat in AdatKezeles.adatok["tantargyak"].values():
            if tantargy.lower() == t_adat['nev'].lower():
                tantargy_id = t_adat['id']
                break

        if not tantargy_id:
            print("Nincs ilyen tantárgy!")
            return

        # Jegy adatainak bekérése
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

        # Tanár ID meghatározása az osztály adataiból
        tanar_id = AdatKezeles.adatok["osztalyok"][diak_osztaly]["tantargyak"][tantargy]["tanar_id"]

        # Új jegy ID generálása
        uj_id = f"J{len(AdatKezeles.adatok['jegyek']) + 1:03d}"

        # Jegy összeállítása
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

        # Jegy mentése
        AdatKezeles.adatok["jegyek"][uj_id] = uj_jegy
        print("\nJegy sikeresen beírva!")

    @staticmethod
    def jegyek_menu():
        print('----------------------------------------------')
        print('Jegy kezelés!')
        print('1. Jegyek Beírása.')
        print('2. Jegyek Listázása Diákonként.')
        print('3. Jegyek Listázása Tantárgyanként.')
        print('4. Átlagok Számítása.')
        print('5. Összes Jegyek Listázása')
        print('6. Vissza a főmenübe')

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
