# Shopify Connector pro Business Central - Přehled Objektů

Vítej, bráško! Tohle je tvůj hlavní rozcestník a dokumentace k **Shopify Connectoru** (standardnímu řešení od Microsoftu pro integraci s Shopify). 

Zdroje jsou načteny z oficiální historie kódu Business Central na GitHubu:
- **Verze/Branch:** `w1-28` (Business Central verze 28 / standardní W1 aplikace)
- **Počet nalezených AL objektů:** 633

## 📂 Členění dokumentace k objektům

| Typ objektu | Popis | Odkaz na detail |
| :--- | :--- | :--- |
| **Tabulky (Tables)** | Definice datového modelu konektoru (nastavení, logy, synchronizovaná data). | [Tabulky a Rozšíření tabulek](shopify_tables.md) |
| **Stránky (Pages)** | Uživatelské rozhraní konektoru (karty obchodu, seznamy, logy, nastavení mapování). | [Stránky a Rozšíření stránek](shopify_pages.md) |
| **Codeunity** | Logika konektoru (volání API, zpracování produktů, zákazníků, objednávek, plateb). | [Codeunity](shopify_codeunits.md) |
| **Reporty (Reports)** | Spouštěče synchronizace a zpracování (exporty/importy zboží, objednávek, zásob atd.). | [Reporty](shopify_reports.md) |
| **Funkční oblasti** | Popis chování klíčových procesů (zboží/varianty, vynechané záznamy, logování). | [Funkční oblasti a procesy](shopify_functional_breakdown.md) |

---

## ⚡ Pokyny pro synchronizaci a aktualizaci
Kdykoliv se mě zeptáš na Shopify Connector, provedu následující:
1. Podívám se na GitHub repository přes lokální sparse-checkout a zkontroluji, zda od posledního stažení nebyly ve složce `Shopify` nějaké aktualizace.
2. Pokud ano, stáhnu je (`git pull`) a automaticky přegeneruji tyto markdown soubory, abych měl vždy aktuální informace.
3. Poté ti odpovím s nejnovějšími fakty.

> [!NOTE]
> Pro zobrazení detailů zdrojového kódu odkazují jednotlivé soubory přímo na oficiální GitHub repozitář s historií kódu Business Central (StefanMaron/MSDyn365BC.Code.History) pro větev `w1-28`.
