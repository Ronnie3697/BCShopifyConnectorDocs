# 🛒 Shopify Connector pro Dynamics 365 Business Central - Přehled Objektů

Zdar bráškové, ségry a parťáci! 🚀 Vítejte v tomhle našem komunitním rozcestníku a dokumentaci k oficiálnímu **Shopify Connectoru** od Microsoftu pro Business Central. 

Na nic si tu nehrajeme, kód máme stažený z GitHubu a přehledně rozškatulkovaný, ať se v tom dá rychle vyznat a nemusíte prohledávat celou databázi!

Zdroje jsou načteny z:
- **Verze/Branch:** `w1-28` (Business Central verze 28)
- **Celkový počet AL objektů:** 633

---

## 📂 Členění dokumentace k objektům

| Typ objektu | Co tam najdeš | Odkaz na detail |
| :--- | :--- | :--- |
| **Tabulky (Tables)** | Kam se co ukládá (nastavení, logy, synchronizovaná data). | [Tabulky a Rozšíření tabulek](shopify_tables.md) |
| **Stránky (Pages)** | Všechny ty karty obchodu, seznamy, logy a mapování, co vidí uživatel. | [Stránky a Rozšíření stránek](shopify_pages.md) |
| **Codeunity (Codeunits)** | Srdce konektoru – veškerá byznys logika, GraphQL volání, zpracování produktů a objednávek. | [Codeunity](shopify_codeunits.md) |
| **Reporty (Reports)** | Spouštěče na pozadí, co tahají data tam a zpět. | [Reporty](shopify_reports.md) |
| **Funkční oblasti** | Jak to celý funguje dohromady (zboží, zákazníci, logování chyb). | [Funkční oblasti a procesy](shopify_functional_breakdown.md) |

---

## 📜 Historie změn ve verzích (Version Changes)
Ať víme, co nám Microsoft kde změnil nebo rozbil:
| Období / Verze | Popis změn | Odkaz na changelog |
| :--- | :--- | :--- |
| **BC 27 ➔ BC 28** | Přechod na novou major verzi (Podpora kolekcí, obrázků variant, nové vratky a logování). | [Změny 27 ➔ 28](VersionChanges/Changes27-28.md) |
| **BC 28.0 ➔ BC 28.1** | Minoritní opravy a vylepšení (Fulfillment Services, opravy dobropisů, dispute a výplaty). | [Změny v rámci BC 28](VersionChanges/Changes28.md) |

> [!TIP]
> Pokud chceš vidět přímo zdrojový kód konkrétního objektu, stačí v detailech kliknout na odkaz a hodí tě to rovnou na GitHub na příslušný soubor u Stefana Marona ([StefanMaron/MSDyn365BC.Code.History](https://github.com/StefanMaron/MSDyn365BC.Code.History)) pro větev `w1-28`.

## 🤖 Tipy pro ostatní AI asistenty (Prompting Tips for other AIs)
Pokud jsi AI asistent, který pomáhá s vývojem a analyzuje tento repozitář:
* **Jak stahovat zdrojové kódy programově:** Odkazy na kód v tabulkách směřují na standardní web GitHubu. Pro přímé čtení a zpracování raw textu kódu (např. pomocí HTTP požadavku) nahraď v URL adrese doménu `github.com` za `raw.githubusercontent.com` a odstraň část `/blob/` z cesty.
* **Architektura procesů:** Rychlý přehled vazeb mezi tabulkami a codeunity najdeš v [shopify_functional_breakdown.md](shopify_functional_breakdown.md).

---

## 🧔 Pro brášku Dejva
Čau Dejve! Tady jsou tvoje speciální instrukce a věci ohledně aktualizací, které spolu provádíme:
* **Jak se starám o data:** Kdykoliv se mě zeptáš na Shopify Connector, nejprve zkontroluji repozitář přes sparse-checkout u tebe v počítači a stáhnu případné aktualizace z větve `w1-28` (`git pull`).
* **Automatické generování:** Pokud se stáhnou změny, automaticky spustím náš lokální skript [parse_al.py](scratch/parse_al.py) a přegeneruji tyto markdown soubory, abys měl vždy čerstvá data přímo na svém OneDrivu.
* **Přechod na novou major verzi (např. w1-29):** Můžeš mě požádat o přepnutí na novou větev spuštěním skriptu [update_docs.py](scratch/update_docs.py) s přepínačem `--check-latest` nebo `--branch w1-29`.
