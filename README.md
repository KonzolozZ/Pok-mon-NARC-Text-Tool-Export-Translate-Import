---

# 🇭🇺 **MAGYAR ÚTMUTATÓ**

---

# Pokémon NARC Szövegkezelő Eszköz 📝🎮

Egy sokoldalú parancssori eszköz a Pokémon Black, White, Black 2 és White 2 játékokban használt `NARC` archívumok szövegeinek exportálására és importálására. Ez az eszköz elengedhetetlen ROM-hackelési projektekhez, különösen a rajongói fordításokhoz.

Helyesen kezeli a játékok által használt egyedi XOR titkosítást, biztosítva, hogy a szövegek tökéletesen dekódolódjanak és újra kódolódjanak, megelőzve ezzel a hibás szövegek megjelenését vagy a játék összeomlását.

## ✨ Funkciók

-   **Kettős Export Mód**: Exportáld a szövegeket egyetlen, könnyen kezelhető `JSON` fájlba, vagy egyedi `.txt` fájlokként egy mappastruktúrába.
-   **Kettős Import Mód**: Importáld vissza a lefordított szövegeket egy `JSON` fájlból vagy egy `.txt` fájlokat tartalmazó mappából.
-   **Helyes Titkosítás**: Az 5. generációs játékokhoz szükséges, pontos XOR titkosítási/dekódolási algoritmust implementálja.
-   **Biztonságos és Megbízható**: Indításkor önellenőrzést végez a kodek integritásának ellenőrzésére, megelőzve a sérült NARC fájlok létrehozását.
-   **Felhasználóbarát Parancssor**: Világos parancssori struktúra, részletes súgó menükkel és példákkal.
-   **Önálló**: Egyetlen Python szkript, külső függőségek nélkül.

## ⚙️ Követelmények

-   Python 3.x

## 🚀 Telepítés

Nincs szükség telepítésre! Ez egy önálló Python szkript.

1.  Töltsd le a szkriptet (`pokemon-text-narc-export-import-tool-hu.py` a magyar verzióhoz vagy `pokemon-text-narc-export-import-tool-en.py` az angolhoz).
2.  Mentsd el a projektmappádba.
3.  Futtasd a terminálból.

## 📖 Hogyan használd

Az eszköz két fő parancs köré épül: `export` és `import`.

### Segítség kérése

A parancsok és példák részletes listáját bármikor elérheted, ha a szkriptet parancs nélkül vagy a `-h` kapcsolóval futtatod.

Általános súgó
python pokemon-text-narc-export-import-tool-hu.py -h

Az 'export' parancs súgója
python pokemon-text-narc-export-import-tool-hu.py export -h

Az 'import' parancs súgója
python pokemon-text-narc-export-import-tool-hu.py import -h


### **1. Lépés: Szövegek exportálása a NARC fájlból**

Két módszer áll rendelkezésedre a szövegek exportálására.

#### **1. Munkamenet: JSON fájl használata (Ajánlott)**

Ez a módszer az összes szöveges bejegyzést egyetlen `.json` fájlba exportálja. Ez a legtisztább módja a fordítások kezelésének.

1.  **Futtasd az export parancsot:**
    ```
    python pokemon-text-narc-export-import-tool-hu.py export a003.narc -o szovegek.json
    ```
    -   `a003.narc` a bemeneti NARC fájlod.
    -   `szovegek.json` lesz a kimeneti fájl.

2.  **Fordítsd le a szövegeket:**
    Nyisd meg a `szovegek.json` fájlt. A következőhöz hasonló struktúrát fogsz látni:
    ```
    {
      "entries": [
        {
          "entry_index": 0,
          "texts": [
            {
              "text_index": 0,
              "original_text": "Pikachu",
              "translated_text": "Pikachu"
            }
          ]
        }
      ]
    }
    ```
    **Fontos:** Csak a `"translated_text"` mező értékét módosítsd. Minden mást hagyj változatlanul.

#### **2. Munkamenet: Egyedi `.txt` fájlok használata**

Ez a módszer minden szöveges bejegyzést saját `.txt` fájlba exportál egy mappastruktúrán belül.

1.  **Futtasd az export parancsot:**
    ```
    python pokemon-text-narc-export-import-tool-hu.py export a003.narc -d szovegfajlok
    ```
    -   Ez létrehoz egy `szovegfajlok` nevű mappát, benne egy `0000` almappával, amely olyan fájlokat tartalmaz, mint `0001.txt`, `0002.txt`, stb.

2.  **Fordítsd le a szövegeket:**
    Nyisd meg az egyes `.txt` fájlokat, és szerkeszd közvetlenül a szöveget.

### **2. Lépés: Szövegek importálása vissza a NARC fájlba**

Miután a fordítások elkészültek, importálhatod őket vissza egy új, módosított NARC fájl létrehozásához.

#### **1. Munkamenet: Importálás JSON fájlból**

1.  **Futtasd az import parancsot:**
    ```
    python pokemon-text-narc-export-import-tool-hu.py import szovegek.json a003.narc uj_a003.narc
    ```
    -   `szovegek.json` a szerkesztett JSON fájlod.
    -   `a003.narc` az eredeti NARC fájl.
    -   `uj_a003.narc` a létrehozandó új, módosított NARC fájl neve.

#### **2. Munkamenet: Importálás `.txt` fájlokat tartalmazó mappából**

1.  **Futtasd az import parancsot:**
    ```
    python pokemon-text-narc-export-import-tool-hu.py import szovegfajlok/ a003.narc uj_a003.narc
    ```
    -   `szovegfajlok/` az a mappa, amely a lefordított `.txt` fájlokat tartalmazza.

Az `uj_a003.narc` fájlod készen áll, hogy visszailleszd a játék ROM-jába!

## 🔧 Technikai Részletek: A XOR Titkosítás

A Pokémon 5. generációs játékok egy speciális, XOR-alapú titkosítást használnak a szövegeik tárolására. Ez az eszköz a pontos, visszafejtett algoritmust implementálja:
1.  Egy kezdő kulcsot (`0x1234`) használ egy kulcssorozat generálásához.
2.  A kulcssorozatot visszafelé generálja, egy `(key >> 3) | (key << 13)` bites eltolásos rotációval.
3.  Egy karakterlánc minden karakterét XOR-olja a sorozat megfelelő kulcsával.
4.  A végére egy kontroll karaktert (`0xFFFF ^ kezdő_kulcs`) fűz.

Ez az eszköz ezt a teljes folyamatot automatikusan kezeli, biztosítva a tökéletes kompatibilitást a játékmotorral.

⚡️ Egy üzenet a Pokémonjaidtól! ⚡️
Eleged van a szövegekből, amik úgy néznek ki, mint egy Tangela gubancos frizurája? Nekünk is! Szóval, elbeszélgettünk egy kicsit az emberekkel.

Psyduck: "Psy-aj-aj?! Fáj a fejem... Az edzők egy új történetet próbálnak olvasni, de a szavak... pont úgy néznek ki, mint amilyen a fejfájásom. Csupa tüske és furcsaság! Nem tudom, hogy a Végzeteset vagy a Farokcsóválást kellene bevetnem!"

Meowth: "Fogd már be, te két lábon járó migrén! A gond nem veled van, hanem azokkal a vacak eszközökkel, amiket az emberek használnak! Annyit érnek, mint egy Magikarp a szárazföldön. De Meowth-nak van egy tuti tippje, egy igazi gyöngyszem: a Pokémon NARC Szövegkezelő Eszköz!

Ez nem akármilyen bigyó. Ismeri a titkos kódot, a különleges kézfogást, az egész hóbelevancot! Fogja azt a sok zagyvaságot, és újra olvasható szavakká alakítja. Ez a tuti befutó, a macskák... nos, egyszerűen szuper!"

Pikachu: "Pika-Pika! (Szuper egyszerű és biztonságos!) Mi magunk teszteltük!

Pika-Pi! (Exportáld az összes játékszöveget!)

Chuuu! (Fordítsd le bármilyen nyelvre, amire csak akarod!)

Pikachu! (Importáld vissza, tökéletesen és csillogóan tisztán, fura jelek nélkül!)"

Meowth: "Ahogy a kis sárga szőrmók mondta! Kiöntheted az összes szöveget egy nagy JSON fájlba, vagy egy csomó apró .txt fájlba. Tiéd a választás! Ez az eszköz okosabb, mint egy Alakazam, aki a saját kanalait próbálja megszámolni. Egyszerűen csak működik!"

Oak professzor: "Khm! Úgy tűnik, ezek a Pokémonok igencsak lelkesek. És jó okkal! Ez az eszköz fantasztikus áttörés minden feltörekvő ROM-hacker és rajongói fordító számára. Kezeli a bonyolult szövegtitkosítást, így ti a tartalom készítésére koncentrálhattok.

A saját Pokémon-kalandotok vár! Töltsétek le a Pokémon NARC Szövegkezelő Eszközt, és kezdjétek el az utazást még ma!"


## ⚖️ Licenc

Ez a projekt a MIT Licenc alatt áll.

---

#### 6️⃣ A projektről

> _Ez a projekt szinte teljes egészében mesterséges intelligencia segítségével készült, de kellett hozzá egy Droid is (vagyis én)!_

---


---

## 🇬🇧 **ENGLISH GUIDE**

---

# Pokémon NARC Text Tool 📝🎮

A versatile command-line tool for exporting and importing text from `NARC` archives used in Pokémon Black, White, Black 2, and White 2. This tool is essential for ROM hacking projects, especially for fan translations.

It correctly handles the unique XOR encryption used by the games, ensuring that texts are decoded and re-encoded perfectly, preventing corrupted text or game crashes.

## ✨ Features

-   **Dual Export Modes**: Export texts into a single, easy-to-manage `JSON` file or as individual `.txt` files in a directory structure.
-   **Dual Import Modes**: Import your translated texts back from either a `JSON` file or a directory of `.txt` files.
-   **Correct Encryption**: Implements the exact XOR encryption/decryption algorithm required for Gen 5 games.
-   **Safe & Reliable**: Includes a self-test on startup to verify the integrity of the codec, preventing corrupted NARC files.
-   **User-Friendly CLI**: Features a clear command structure with detailed help menus and examples.
-   **Standalone**: A single Python script with no external dependencies.

## ⚙️ Requirements

-   Python 3.x

## 🚀 Installation

No installation is required! This is a standalone Python script.

1.  Download the script (`pokemon-text-narc-export-import-tool-en.py` for English or `pokemon-text-narc-export-import-tool-hu.py` for Hungarian).
2.  Save it to your project folder.
3.  Run it from your terminal.

## 📖 How to Use

The tool operates using two main commands: `export` and `import`.

### Getting Help

You can get a detailed list of commands and examples at any time by running the script without a command or with the `-h` flag.

General help
python pokemon-text-narc-export-import-tool-en.py -h

Help for the 'export' command
python pokemon-text-narc-export-import-tool-en.py export -h

Help for the 'import' command
python pokemon-text-narc-export-import-tool-en.py import -h


### **Step 1: Exporting Texts from the NARC file**

You have two methods for exporting texts.

#### **Workflow 1: Using a JSON file (Recommended)**

This method exports all text entries into a single `.json` file. It's the cleanest way to manage translations.

1.  **Run the export command:**
    ```
    python pokemon-text-narc-export-import-tool-en.py export a003.narc -o texts.json
    ```
    -   `a003.narc` is your input NARC file.
    -   `texts.json` will be your output file.

2.  **Translate the texts:**
    Open `texts.json`. You will see a structure like this:
    ```
    {
      "entries": [
        {
          "entry_index": 0,
          "texts": [
            {
              "text_index": 0,
              "original_text": "Pikachu",
              "translated_text": "Pikachu"
            }
          ]
        }
      ]
    }
    ```
    **Important:** Only modify the value of the `"translated_text"` field. Leave everything else unchanged.

#### **Workflow 2: Using individual `.txt` files**

This method exports each text entry into its own `.txt` file within a directory structure.

1.  **Run the export command:**
    ```
    python pokemon-text-narc-export-import-tool-en.py export a003.narc -d text_files
    ```
    -   This will create a directory named `text_files` with a `0000` subdirectory containing files like `0001.txt`, `0002.txt`, etc.

2.  **Translate the texts:**
    Open each `.txt` file and edit the text directly.

### **Step 2: Importing Texts back into the NARC file**

Once your translations are complete, you can import them back to create a new, modified NARC file.

#### **Workflow 1: Importing from a JSON file**

1.  **Run the import command:**
    ```
    python pokemon-text-narc-export-import-tool-en.py import texts.json a003.narc new_a003.narc
    ```
    -   `texts.json` is your edited JSON file.
    -   `a003.narc` is the original NARC file.
    -   `new_a003.narc` is the name of the new, modified NARC file that will be created.

#### **Workflow 2: Importing from a directory of `.txt` files**

1.  **Run the import command:**
    ```
    python pokemon-text-narc-export-import-tool-en.py import text_files/ a003.narc new_a003.narc
    ```
    -   `text_files/` is the directory containing your translated `.txt` files.

Your `new_a003.narc` file is now ready to be inserted back into your game ROM!

## 🔧 Technical Details: The XOR Encryption

Pokémon Gen 5 games use a specific XOR-based encryption to store their text. This tool implements the exact reverse-engineered algorithm:
1.  A seed key (`0x1234`) is used to generate a sequence of keys.
2.  The key sequence is generated backwards, using a `(key >> 3) | (key << 13)` bit shift rotation.
3.  Each character in a string is XORed with its corresponding key in the sequence.
4.  A final control character (`0xFFFF ^ seed_key`) is appended to the end.

This tool handles this entire process automatically, ensuring perfect compatibility with the game engine.


⚡️ A Message From Your Pokémon! ⚡️
Tired of text that looks like a Tangela's bad hair day? We were too! So we had a little chat with the humans.

Psyduck: "Psy-ay-ay?! My head hurts... The trainers are trying to read a new story, but the words... they look like my headache feels. All spiky and weird! I can't tell if I'm supposed to use Tackle or Tail Whip!"

Meowth: "Pipe down, ya walking migraine! The problem ain't you, it's the tools the humans are usin'! They're about as effective as a Magikarp on dry land. But Meowth's got the inside scoop on a real gem: the Pokémon NARC Text Tool!

This ain't no ordinary doohickey. It knows the secret code, the special handshake, the whole shebang! It takes all that garbled nonsense and turns it back into words you can actually read. It’s the top banana, the cat’s meow, the... well, it’s just really, really good!"

Pikachu: "Pika-Pika! (It's super easy and safe!) We tested it ourselves!

Pika-Pi! (Export all the game text!)

Chuuu! (Translate it into any language you want!)

Pikachu! (Import it back in, perfect and sparkly clean, with no weird symbols!)"

Meowth: "What the little yellow fella said! You can dump all the text into one big JSON file, or into lots of little .txt files. Your choice! This tool is smarter than an Alakazam trying to count its own spoons. It just works!"

Professor Oak: "Ahem! It seems these Pokémon are quite enthusiastic. And for good reason! This tool is a fantastic breakthrough for all you aspiring ROM hackers and fan translators out there. It handles the complex text encryption so you can focus on creating.

Your own Pokémon adventure is waiting! Download the Pokémon NARC Text Tool and start your journey today!"


## ⚖️ License

This project is licensed under the MIT License.

---

#### 6️⃣ About this project

> _This project was almost entirely created with AI, but it still needed a Droid’s helping hand (that’s me)!_

---
