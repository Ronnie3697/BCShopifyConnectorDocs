# 🛒 Shopify Connector pro Dynamics 365 Business Central - Přehled Objektů

Zdar bráškové, ségry a parťáci! 🚀 Vítejte v tomhle našem komunitním rozcestníku a dokumentaci k oficiálnímu **Shopify Connectoru** od Microsoftu pro Business Central. 

Na nic si tu nehrajeme, kód máme stažený z GitHubu a přehledně rozškatulkovaný, ať se v tom dá rychle vyznat a nemusíte prohledávat celou databázi!

Zdroje jsou načteny z:

- **Zdroj/Branch:** [microsoft/BCApps](https://github.com/microsoft/BCApps/tree/releases/29.0/src/Apps/W1/Shopify), `releases/29.0`
- **Aktuální verze:** `29.0` (verze v `App/app.json`: `29.0.0.0`, synchronizováno 2026-10-19)
- **Snapshot zdrojů:** [`28896630`](https://github.com/microsoft/BCApps/commit/288966302f7be8f3fe08f02cde0059a4c4a7f4a7) (výchozí bod 29.0 byl [`84f94fce`](https://github.com/microsoft/BCApps/commit/84f94fce9754c8d1c9440dc62885ff33788778ae)). Jde o release zdrojový kód; číslo konkrétního distribuovaného buildu ani dostupnost aktualizace v tenantech z něj neurčujeme.
- **Celkový počet AL objektů:** 509 (včetně enumů, interfaců a permission setů; v 28.5 jich bylo 639 — 129 GQL codeunitů nahradily `.graphql` resource soubory)
- **Dokumentace BC 28:** poslední stav 28.5 je v historii repa ([commit `b0db0b2`](https://github.com/Ronnie3697/BCShopifyConnectorDocs/tree/b0db0b2)), změny popisuje [Changes28.md](VersionChanges/Changes28.md).

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
| **BC 28.0 ➔ BC 28.5** | Minoritní updaty: 28.1 (Fulfillment Services, dobropisy, disputy), 28.2 (compareAtPrice), 28.3 (B2B pro všechny plány), 28.4 (pending refund transakce, měny), 28.5 (přesné párování zákazníků, filtry katalogů, export variant). | [Změny v rámci BC 28](VersionChanges/Changes28.md) |
| **BC 28 ➔ BC 29** | Přechod na novou major verzi (expirující tokeny, GraphQL dotazy v resource souborech, API 2026-07, číslo Shopify objednávky jako číslo dokladu, vratkové objednávky, HS kódy, stav Unlisted, daňové údaje objednávek). | [Změny 28 ➔ 29](VersionChanges/Changes28-29.md) |
| **BC 29.0 ➔ …** | Minoritní updaty BC 29: servisní oprava 29.0 (párování daní jen pro US/CA, `Shpfy Order Tax Line.Title` na Code[100]). | [Změny v rámci BC 29](VersionChanges/Changes29.md) |

**Nově v 29.0:** [Změny 28 ➔ 29, sekce „Co musí řešit vývojáři rozšíření a provoz"](VersionChanges/Changes28-29.md) — hlavně **expirující tokeny**: Shopify od 2027-01-01 odmítne neexpirující tokeny a migraci má zatím jen BC 29 (v `releases/28.x` k 2026-10-02 není).

> [!TIP]
> Odkazy u objektů vedou přímo do oficiálního [microsoft/BCApps](https://github.com/microsoft/BCApps/tree/releases/29.0/src/Apps/W1/Shopify) na větev `releases/29.0`. Starší changelogy zachovávají původní zdroj StefanMaron/MSDyn365BC.Code.History; jeho větev `w1-28` při přechodu na BCApps (2026-09-07) končila buildem 28.4.53241.0.

## 🤖 Tipy pro ostatní AI asistenty (Prompting Tips for other AIs)
Pokud jsi AI asistent, který pomáhá s vývojem a analyzuje tento repozitář:
* **Jak stahovat zdrojové kódy programově:** Odkazy na kód v tabulkách směřují na standardní web GitHubu. Pro přímé čtení a zpracování raw textu kódu (např. pomocí HTTP požadavku) nahraď v URL adrese doménu `github.com` za `raw.githubusercontent.com` a odstraň část `/blob/` z cesty.
* **Architektura procesů:** Rychlý přehled vazeb mezi tabulkami a codeunity najdeš v [shopify_functional_breakdown.md](shopify_functional_breakdown.md).
* **Oficiální in-repo dokumentace:** Od BC 29 má konektor v BCApps vlastní `App/CLAUDE.md` a [App/docs](https://github.com/microsoft/BCApps/tree/releases/29.0/src/Apps/W1/Shopify/App/docs) (`business-logic.md`, `data-model.md`, `extensibility.md`, `patterns.md`) a v oblastech `src/<Oblast>/docs/`. Pro eventy a body rozšíření je to nejlepší zdroj.
* **GraphQL dotazy:** Od BC 29 nejsou v codeunitech, ale v `App/.resources/graphql/<Oblast>/<Dotaz>.graphql`.

---

## 🧔 Pro brášku Dejva
Čau Dejve! Tady jsou tvoje speciální instrukce a věci ohledně aktualizací, které spolu provádíme:
* **Jak se starám o data:** Kdykoliv se mě zeptáš na Shopify Connector, nejprve zkontroluji sparse-checkout Microsoft BCApps (`%LOCALAPPDATA%\BCShopifyConnectorDocs\bcapps`, vytvoří se sám — schválně mimo OneDrive) a stáhnu případné aktualizace z větve `releases/29.0`. Původní checkout `msdyn` zůstává pro historická porovnání.
* **Automatické generování:** Celý update obstará skript [update_docs.py](scratch/update_docs.py) — stáhne novinky a přes [parse_al.py](scratch/parse_al.py) přegeneruje markdown soubory, abys měl vždy čerstvá data přímo v `C:\WorkTasks\BCShopifyConnectorDocs`. Spuštění: `python scratch/update_docs.py`.
* **Přechod na další verzi:** `python scratch/update_docs.py --check-latest` zjistí nejnovější číselnou release větev (ignoruje průběžné větve typu `releases/29.x`). Přepnutí například na `--branch releases/29.1` použij, až bude větev existovat. Při trvalém přechodu uprav také `DEFAULT_BRANCH` v updateru a výchozí `--branch` v parseru, metadata tohoto README a changelog; samotný přepínač mění jen aktuální běh. Existence větve sama nepotvrzuje vydání aktualizace pro tenanty.
* **Changelogy minor verzí:** Po každém updatu doplň [VersionChanges/Changes29.md](VersionChanges/Changes29.md) — diffy mezi verzemi vypíše `update_docs.py` na konci běhu. Při přechodu na major verzi vznikne nový `ChangesXX-YY.md` (diff proti poslední minor verzi předchozí major) a `ChangesYY.md` s výchozím snapshotem.
* **⚠️ Windows pozor:** checkout potřebuje `git config core.longpaths true` (dlouhé cesty ve složce `Order Return Refund Processing` se jinak tiše nevytvoří a v dokumentaci pak chybí ~20 objektů) — skript to nastavuje automaticky.

## ⚠️ Co konektor nemá a co je z PTE nedostupné (poznatky z praxe)

- **Discount API konektor neimplementuje** (žádné `discountCodeBasicCreate` / `discountCodeDeactivate`; jen čtení slev
  při importu objednávek přes `GetTotalLineDiscountAmount`).
- **Komunikační vrstva je `Access = Internal`:** `Shpfy Communication Mgt.` (30103, `ExecuteGraphQL`), enum
  `Shpfy GraphQL Type` (30111; od BC 29 navíc `Extensible = false`) i `Shpfy Authentication Mgt.` (30199); access i refresh
  token leží v Isolated Storage konektoru se scope `Module`. Vlastní GraphQL mutace z jiné appky = **vlastní HttpClient +
  vlastní custom app / token** (platí i pro BC 29.0).
- **`Shpfy Shop` je public, ale `"Shopify URL"` a `GetStoreName`/`SetStoreName` jsou Internal** (`AL0161`) — adresu shopu
  si musí PTE držet ve vlastním poli. Ověřeno 2026-09-22 na 28.4.53241.53839 (cust-sonnentor-bc 63637, slevové kódy
  dárkových poukazů; návrh `docs/proposals/63637-shopify-voucher-discounts.md`), ve zdrojích 29.0 beze změny.
- **Testovací mocking přes eventy konektoru v BC 29 zmizel** (`Shpfy Communication Events`, `IsTestInProgress`) — testy
  rozšíření mockují HTTP přes platformní `[HttpClientHandler]`.
