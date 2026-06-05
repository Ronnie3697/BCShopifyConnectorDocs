# Shopify Connector pro Dynamics 365 Business Central - Přehled Objektů

Tento repozitář obsahuje komplexní, strukturovanou a automaticky generovanou dokumentaci k **Shopify Connectoru** (standardnímu řešení od společnosti Microsoft pro integraci Dynamics 365 Business Central s platformou Shopify).

Zdroje a objekty jsou načteny z oficiální historie kódu Business Central:
- **Verze/Branch:** `w1-28` (Business Central verze 28 / standardní W1 aplikace)
- **Celkový počet AL objektů:** 633

## 📂 Členění dokumentace k objektům

| Typ objektu | Popis | Odkaz na detail |
| :--- | :--- | :--- |
| **Tabulky (Tables)** | Definice datového modelu konektoru (nastavení, logy, synchronizovaná data). | [Tabulky a Rozšíření tabulek](shopify_tables.md) |
| **Stránky (Pages)** | Uživatelské rozhraní konektoru (karty obchodu, seznamy, logy, nastavení mapování). | [Stránky a Rozšíření stránek](shopify_pages.md) |
| **Codeunity (Codeunits)** | Logika konektoru (volání API, zpracování produktů, zákazníků, objednávek, plateb). | [Codeunity](shopify_codeunits.md) |
| **Reporty (Reports)** | Spouštěče synchronizace a zpracování (exporty/importy zboží, objednávek, zásob atd.). | [Reporty](shopify_reports.md) |
| **Funkční oblasti** | Popis chování klíčových procesů (zboží/varianty, vynechané záznamy, logování). | [Funkční oblasti a procesy](shopify_functional_breakdown.md) |

---

## 📜 Historie změn ve verzích (Version Changes)
| Období / Verze | Popis změn | Odkaz na changelog |
| :--- | :--- | :--- |
| **BC 27 ➔ BC 28** | Přechod na novou major verzi (Podpora kolekcí, obrázků variant, přepracované vratky a logování). | [Změny 27 ➔ 28](VersionChanges/Changes27-28.md) |
| **BC 28.0 ➔ BC 28.1** | Minoritní opravy a vylepšení (Fulfillment Services, opravy dobropisů, logování, dispute a výplaty). | [Změny v rámci BC 28](VersionChanges/Changes28.md) |

> [!NOTE]
> Pro zobrazení detailů zdrojového kódu odkazují jednotlivé soubory přímo na oficiální GitHub repozitář s historií kódu Business Central ([StefanMaron/MSDyn365BC.Code.History](https://github.com/StefanMaron/MSDyn365BC.Code.History)) pro větev `w1-28`.

---

## 🧔 Pro brášku Dejva
Čau Dejve! Tady jsou tvoje speciální instrukce a věci ohledně aktualizací, které spolu provádíme:
* **Jak se starám o data:** Kdykoliv se mě zeptáš na Shopify Connector, nejprve zkontroluji repozitář přes sparse-checkout u tebe v počítači a stáhnu případné aktualizace z větve `w1-28` (`git pull`).
* **Automatické generování:** Pokud se stáhnou změny, automaticky spustím náš lokální skript [parse_al.py](scratch/parse_al.py) a přegeneruji tyto markdown soubory, abys měl vždy čerstvá data přímo na svém OneDrivu.
* **Přechod na novou major verzi (např. w1-29):** Můžeš mě požádat o přepnutí na novou větev spuštěním skriptu [update_docs.py](scratch/update_docs.py) s přepínačem `--check-latest` nebo `--branch w1-29`.
