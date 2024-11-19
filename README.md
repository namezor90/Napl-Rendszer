# 🏫 Iskolai Rendszerkezelő

Egy átfogó Python alapú iskolai rendszer diákok, tanárok, osztályok és jegyek kezelésére.

## ✨ Funkciók

### 📚 Jelenlegi Funkciók
- 👨‍🏫 Teljes tanári adminisztráció
- 👥 Diák nyilvántartás
- 📊 Osztálykezelés
- 📝 Jegykezelés és elemzés
- 📅 Jelenlét követés
- 🔄 Többszintű menürendszer
- 💾 JSON alapú adattárolás

### 🔮 Tervezett Funkciók
- ✏️ Adat módosítás és törlés
- 📈 Bővített jelentések és elemzések
- 🔒 Felhasználói hitelesítés
- 💾 Biztonsági mentés
- 📤 Adat exportálás

## 🛠️ Rendszer Komponensek

### 👨‍🏫 Tanár Kezelés
- Új tanár felvétele/megtekintése
- Tanítási beosztások kezelése
- Osztályfőnöki feladatok
- Végzettségek és elérhetőségek

### 👨‍🎓 Diák Kezelés
- Diák beiratkozás és nyilvántartás
- Szülői kapcsolattartási adatok
- Hiányzások követése
- Tanulmányi előmenetel

### 📚 Osztály Kezelés
- Órarend
- Tantárgyak hozzárendelése
- Tanárok beosztása
- Diáklista kezelés

### 📝 Jegy Kezelés
- Jegyek rögzítése
- Átlagok számítása (diák/osztály/tantárgy)
- Teljesítmény jelentések
- Jegynapló vezetés

### 💾 Adatszerkezet
JSON adatbázis főbb gyűjteményei:
- Tanárok (`tanarok`)
- Diákok (`diakok`) 
- Osztályok (`osztalyok`)
- Tantárgyak (`tantargyak`)
- Jegyek (`jegyek`)
- Statisztikák (`statisztikak`)

## 🚀 Használat

### 📋 Követelmények
- Python 3.10+
- JSON modul

### 🎯 Program Indítása
```python
python main2.py
```

### 📱 Főmenü Opciók
1. Tanárok Kezelése
2. Diákok Kezelése
3. Osztályok Kezelése
4. Tantárgyak Kezelése
5. Jegyek Kezelése
6. Kilépés

## 📊 Adatmodell

### 👨‍🏫 Tanár Rekord Példa
```json
{
  "id": "T001",
  "nev": "Kiss János",
  "tantargyak": ["matematika"],
  "osztalyfonok": "9.A",
  "tanitott_osztalyok": ["9.A", "10.B"],
  "vegzettseg": "matematika-fizika szakos tanár"
}
```

### 👨‍🎓 Diák Rekord Példa
```json
{
  "id": "D001",
  "nev": "Kiss Pista",
  "osztaly_id": "9.A",
  "szulok": {
    "anya": {
      "nev": "Kiss Márta",
      "telefonszam": "+36201234567"
    }
  },
  "hianyzasok": {
    "igazolt": 12,
    "igazolatlan": 0
  }
}
```

## 🎯 Fejlesztési Ütemterv

### 📍 1. Fázis (Jelenlegi)
- ✅ Alap adatstruktúrák
- ✅ Menürendszer
- ✅ Megtekintési funkciók
- ⏳ Adat módosítási funkciók

### 📍 2. Fázis (Tervezett)
- 🔒 Felhasználói hitelesítés
- 📊 Bővített jelentések
- ✅ Adatellenőrzés
- ⚠️ Hibakezelés
- 🖥️ Grafikus felület

### 📍 3. Fázis (Jövőbeli)
- 💾 Adatbázis migráció
- 🔌 API fejlesztés
- 📱 Mobilalkalmazás integráció
- 📊 Fejlett analitika

## 🤝 Közreműködés

A projekt aktív fejlesztés alatt áll. Közreműködés esetén kérjük:
1. Kövesse a meglévő kódstruktúrát
2. Adjon magyarázatot a komplex logikához
3. Frissítse a dokumentációt új funkciók esetén
4. Alaposan teszteljen minden változtatást

## 📝 Megjegyzések

- 🇭🇺 A rendszer magyar nyelvű menüket és adatokat használ
- 📅 Minden dátum ÉÉÉÉ-HH-NN formátumú
- 💾 A JSON adatbázis indításkor töltődik be
- 🔄 A jövőbeli verziók tartalmazni fognak adatmentést
