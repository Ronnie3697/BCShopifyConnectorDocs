# Shopify Connector - Změny v rámci verze BC 28 (Changes 28 - Minor Updates)

Tento dokument detailně popisuje změny a minoritní aktualizace v **Shopify Connectoru** v rámci verze **Business Central 28** (postupné přechody **28.0 ➔ 28.1 ➔ 28.2 ➔ 28.3 ➔ 28.4 ➔ 28.5**).

---

## 🔄 Změny 28.0 ➔ 28.1 (květen 2026, build 28.1.49838.49886)

### 📊 Základní statistika změn
* **Počet změněných souborů:** 23
* **Přidané řádky (Insertions):** 265
* **Smazané řádky (Deletions):** 29

### 1. ⚙️ Kontrola a mapování služeb plnění (Fulfillment Services)
* **Nový GraphQL check:** Přidán codeunit pro ověření, zda je dané Shopify umístění nakonfigurováno jako fulfillment služba.
* **Přidané objekty:**
  * Codeunit: `Shpfy GQL HasFFService` (ID 30303)
* **Změny chování:** Ve `Shpfy Sync Shop Locations` (ID 30105) byla upravena synchronizace, která nyní dynamicky zohledňuje, zda je lokace typu Fulfillment Service.

### 2. 📝 Karta obchodu a UX úpravy (Shop Card & Lists)
* **Nová pole a akce:** 
  * Na stránce `Shpfy Shop Card` (ID 30101) a seznamu `Shpfy Shops` (ID 30102) byly přidány nové vizuální prvky a akce, které usnadňují správu synchronizace.
  * Přidána možnost zobrazit a spravovat historii dávkových úloh (Bulk Operations) přímo z přehledů.
* **Úpravy v souborech:**
  * `Shpfy Shop Card.Page.al`
  * `Shpfy Shops.Page.al`
  * `Shpfy Bulk Operations.Page.al`

### 3. 👥 Export zákazníků (Customer Export)
* **Oprava a vylepšení logiky:** Ve `Shpfy Customer Export` (ID 30113) byly upraveny podmínky pro filtrování a export zákaznických dat, což zamezuje duplicitám a nekonzistencím při změnách adres.

### 4. ↩️ Zaúčtování refundací (Refunds Creation)
* **Oprava chyb:** V codeunitu `Shpfy Create Sales Doc. Refund` (ID 30140) došlo k opravě a zpřesnění logiky pro zakládání prodejních dobropisů v BC na základě Shopify refundací, zejména pro případy, kdy se vrací pouze doprava (shipping charges) nebo dárkové karty (gift cards).

### 5. 💵 Disputy a výplaty (Disputes & Payouts)
* **Zpřesnění datového modelu:**
  * Do tabulky `Shpfy Dispute` (ID 30141) byla přidána nová pole pro lepší sledování stavu sporů (Disputes).
  * V tabulce `Shpfy Payout` (ID 30138) byla upravena a opravena struktura výpočtu poplatků a čistých částek pro výplaty.

---

## 🔄 Změny 28.1 ➔ 28.2 (červen 2026, build 28.2.50931.51034)

### 📊 Základní statistika změn
* **Počet změněných souborů:** 2 (+ verzování app.json)
* **Přidané řádky (Insertions):** 10
* **Smazané řádky (Deletions):** 9

### 1. 💰 Oprava `compareAtPrice` v hromadné aktualizaci cen (Bulk Operations)
* **Oprava chyby:** Při hromadné aktualizaci cen variant (Bulk Operation) se porovnávací cena (`compareAtPrice`) posílala do Shopify vždy — i když se neměnila, posílala se hodnota `0`, což v Shopify porovnávací cenu nechtěně mazalo/přepisovalo.
* **Nové chování:** Fragment `"compareAtPrice"` se do JSON payloadu vkládá **jen pokud se hodnota reálně změnila**:
  * změna na konkrétní hodnotu ➔ pošle se `"compareAtPrice": "<hodnota>"`,
  * smazání porovnávací ceny ➔ pošle se explicitní `"compareAtPrice": null`,
  * beze změny ➔ pole se v payloadu vůbec neobjeví a Shopify zachová stávající hodnotu.
* **Upravené objekty:**
  * Codeunit: `Shpfy Bulk UpdateProductPrice` (ID 30281) — šablona vstupního JSONu (`GetInput`)
  * Codeunit: `Shpfy Variant API` (ID 30189) — sestavení fragmentu při detekci změny

---

## 🔄 Změny 28.2 ➔ 28.3 (červenec 2026, build 28.3.52162.52222)

### 📊 Základní statistika změn
* **Počet změněných souborů:** 7 (+ verzování app.json)
* **Přidané řádky (Insertions):** 69
* **Smazané řádky (Deletions):** 28

### 1. 🏢 B2B funkce pro všechny Shopify plány (nové pole „Advanced Shopify Plan")
* **Změna konceptu:** Shopify zpřístupnilo B2B funkce na všech plánech, takže pole `B2B Enabled` ztratilo smysl jako přepínač celého B2B.
* **Obsolete:** Pole `B2B Enabled` (tabulka `Shpfy Shop` ID 30102, field 117) je označeno **ObsoleteState = Pending** (odstranění ve verzi 29.0/32.0 dle CLEANSCHEMA) s důvodem *„B2B features are now available on all Shopify plans."*
* **Náhrada:** Nové pole `Advanced Shopify Plan` (field 207) — nastavuje se automaticky podle plánu obchodu (Shopify Plus, Plus Trial, Development, **nově i Advanced**) při načtení informací o obchodě.
* **Upgrade:** `Shpfy Upgrade Mgt.` (ID 30106) obsahuje novou upgrade proceduru, která přes `DataTransfer` překlopí `B2B Enabled = true` ➔ `Advanced Shopify Plan = true` (upgrade tag `MS-630316-HasAdvancedShopifyPlanUpgrade-20260408`).

### 2. 📝 Karta obchodu a Activities — B2B už není schované
* Skupina **B2B Company Synchronization**, akce **Companies**, **Market Catalogs** a synchronizace firem na `Shpfy Shop Card` (ID 30101) už **nejsou skryté** za `B2B Enabled` — zobrazují se vždy.
* Akce **Catalogs** a **Staff Mapping** se nově řídí polem `Advanced Shopify Plan`.
* Akce **Sync All** nově spouští `CompanySync` a `CatalogPricesSync` **vždy** (dříve jen při zapnutém B2B).
* Na `Shpfy Activities` (ID 30100) je cue **Unmapped Companies** viditelná vždy.
* Pole `Auto Create Catalog` má nový caption **„Auto Create B2B Catalog"** a validaci — jde zapnout jen pro plány Shopify Plus, Plus Trial, Development nebo Advanced (nová chybová hláška).

### 3. 📦 Import objednávek a Staff Members dle plánu
* `Shpfy Import Order` (ID 30161) a `Shpfy Staff Member API` (ID 30105) nově podmiňují načítání `staffMember` z GraphQL polem `Advanced Shopify Plan` místo `B2B Enabled`.

### 4. 🏢 Oprava exportu firem v multi-shop prostředí (Company Export)
* **Oprava chyby:** `Shpfy Company Export` (ID 30284) při kontrole „firma s tímto External Id už existuje" nefiltroval na `Shop Code`. Při více obchodech v jedné databázi tak zákazník exportovaný do druhého obchodu skončil chybně jako *skipped record*. Nově se kontrola omezuje na aktuální obchod.

---

## 🔄 Změny 28.3 ➔ 28.4 (srpen 2026, build 28.4.53241.0)

### 📊 Základní statistika změn
* **Počet změněných souborů:** 8 (+ verzování app.json)
* **Přidané řádky (Insertions):** 68
* **Smazané řádky (Deletions):** 12

### 1. ↩️ Refundy s nedokončenými transakcemi (Pending Refund Transactions)
* **Nový check:** `Shpfy Refunds API` (ID 30228) má novou proceduru `HasPendingRefundTransactions` — dokud má refund v Shopify aspoň jednu transakci ve stavu **Pending**, hlásí Shopify refundovanou částku 0 a vytvořený dobropis by se vynuloval vyrovnávacím řádkem.
* **Nové chování:**
  * Ruční vytvoření dobropisu z refundu s pending transakcí skončí novou chybovou hláškou (zkusit znovu po dokončení transakcí).
  * Automatické zpracování `Shpfy RetRefProc Cr.Memo` (ID 30243) takový refund **tiše přeskočí** a zpracuje ho v dalším běhu.
* **Datový model:** Tabulka `Shpfy Order Transaction` (ID 30133) má nový klíč `Refund Id, Type, Status` pro rychlé vyhledání pending refund transakcí.

### 2. 💱 Robustnější mapování měny při importu objednávek
* `Shpfy Import Order` (ID 30161) — přepsané hledání měny podle ISO kódu ze Shopify:
  * rychlá cesta: kód odpovídá LCY z General Ledger Setup ➔ prázdný kód měny,
  * při **více měnách se stejným ISO kódem** nebo **nenalezené měně** se loguje telemetrie (warning) a použije se první nalezená měna, resp. fallback `Currency.Get` na samotný kód,
  * ošetřen edge case, kdy je LCY nakonfigurováno jako ne-ISO kód.
* **Měna transakcí:** `Shpfy Transactions` (ID 30194) nově ukládá i `amountSet.shopMoney.currencyCode` do pole `Currency` tabulky `Shpfy Order Transaction`.

### 3. 💰 Ochrana proti chybějícímu `unitCost` v odpovědi Shopify
* `Shpfy Product Export` (ID 30178) a `Shpfy Bulk UpdateProductPrice` (ID 30281) čtou `unitCost` z JSON odpovědi **jen pokud klíč existuje** — dřív chybějící klíč shodil zpracování.

### 4. 🔓 Zpřístupnění `Shpfy Update Price Source`
* Codeunit `Shpfy Update Price Source` (ID 30272) změněn z `Access = Internal` na **`Access = Public`** — subscribery pro výpočet cen dle Shopify zákazníka jde nově využít i z vlastních rozšíření.

---
## BC 28.4 → BC 28.5

Ověřeno 2026-09-07 proti oficiálním zdrojům [microsoft/BCApps, releases/28.5](https://github.com/microsoft/BCApps/tree/releases/28.5/src/Apps/W1/Shopify). Verze v `App/app.json` je **28.5.0.0**; není to číslo konkrétního distribuovaného buildu ani potvrzení dostupnosti aktualizace v tenantech.

### Rozsah porovnání

- Oficiální snapshot 28.4: `d3f232623dfc4ff577f26222a9eb7fd261df25cf`.
- Oficiální snapshot 28.5: `278c96d3a8d4d691137f14febae59816a8bf616f`.
- [Diff těchto snapshotů](https://github.com/microsoft/BCApps/compare/d3f232623dfc4ff577f26222a9eb7fd261df25cf...278c96d3a8d4d691137f14febae59816a8bf616f): pro statistiku zde je použit přímý `git diff <28.4-sha> <28.5-sha> -- src/Apps/W1/Shopify` (webový compare může zobrazovat rozdíl od společného předka).
- V celé složce Shopify **12 změněných souborů, +399 / −51 řádků**, včetně manifestů, testů a jejich JSON odpovědí.
- V produkčním `App/src` **6 změněných AL souborů, +74 / −41 řádků**. Počet objektů zůstává **639**, žádný AL objekt nepřibyl ani nezmizel.

### 1. Přesnější párování zákazníků podle e-mailu a telefonu

`Shpfy Customer API` (codeunit 30114) nyní kontroluje i hodnotu vrácenou vyhledáváním Shopify. Samotný první výsledek už nestačí: e-mail musí přesně odpovídat po převodu na malá písmena, telefon po odstranění znaků kromě číslic a `+`. Telefon obsahující mezery, závorky či pomlčky se tak porovnává bez těchto oddělovačů. Nesouhlasící výsledek vrací ID `0`; nehrozí přijetí pouze částečné shody z tokenizovaného vyhledávání.

GraphQL codeunity `Shpfy GQL FindCustByEMail` (30129) a `Shpfy GQL FindCustByPhone` (30130) proto nově žádají také `defaultEmailAddress.emailAddress` a `defaultPhoneNumber.phoneNumber`; očekávaná cena dotazu stoupla z 3 na 4. Vyhledávání stále používá `customers(first: 1)`, takže změna nepřidává procházení dalších výsledků. Normalizace telefonu nedoplňuje předvolbu země.

Zdroj: [oprava párování zákazníků (#10621)](https://github.com/microsoft/BCApps/commit/bc180c9d).

### 2. Filtrování katalogů při synchronizaci cen

Report `Shpfy Sync Catalog Prices` (30116) má pod obchodem nový dataitem katalogu s filtry **Id** a **Name**. Lze tak omezit synchronizaci na vybrané katalogy a rozdělit rozsáhlé B2B zpracování. Nadále se zpracovávají pouze katalogy s povoleným `Sync Prices` a uplatňují se nastavené filtry firmy a typu katalogu.

Codeunit stejného názvu (30295) už nemá `TableNo` ani zpracování v `OnRun`; report nastavuje obchod přes `SetShop` a předává jednotlivé katalogy do nové interní procedury `SyncCatalog`. Codeunit si pamatuje zpracovaná ID katalogů a při nastavení obchodu seznam vymaže. Původní interní `SetCompanyId` zmizelo, filtr je v reportu. Při údržbě vlastního forku je tedy potřeba prověřit případná přímá volání této codeunity.

Změna reaguje na překročení dvanáctihodinového limitu rozsáhlé synchronizace; sama nezaručuje dokončení libovolně velké dávky. Zdroj: [filtry synchronizace cen katalogů (#10296)](https://github.com/microsoft/BCApps/commit/806d2999).

### 3. Export variant po „Add Item as Shopify Variant“

`Shpfy Product Export` (codeunit 30178) před hledáním chybějících variant znovu načte hlavní zboží podle `Shpfy Product."Item SystemId"`. Smyčka aktualizující existující Shopify varianty totiž mohla ponechat v proměnné `Item` jiné zboží, přidané jako varianta produktu. Export potom nesprávně vytvářel i jeho další, nenamapované varianty.

V 28.5 se chybějící varianty a měrné jednotky hledají opět vůči hlavnímu zboží produktu. Pokud hlavní zboží neexistuje, tato část exportu skončí. Zdroj: [oprava exportu variant (#8615)](https://github.com/microsoft/BCApps/commit/06255643).

### Testy v upstreamu

Microsoft přidal šest regresních testů: pět pro normalizaci telefonu, odmítnutí částečné shody a přijetí přesné shody telefonu/e-mailu; jeden pro export produktu s jiným zbožím namapovaným jako varianta. Test exportu ověřuje, že se nepřidá jeho další nenamapovaná varianta. Při této aktualizaci dokumentace byly testy přečteny, nebyly spouštěny v BC.

### Rozdíl proti předchozí dokumentaci 28.4

Dosavadní dokumentace vycházela z buildu **28.4.53241.0** v repozitáři StefanMaron/MSDyn365BC.Code.History (`271a0b6020d22eda93437f10723cee5c8cb064ba`). Proti tomuto staršímu snapshotu se v nynějším `App/src` změnilo **7 AL souborů**, nikoli jen šest z přímého porovnání oficiálních větví výše.

Dodatečná změna je v `Shpfy Authentication Mgt.` (codeunit 30199): odpověď OAuth obsahující přístupový token se již nepředává do laditelné procedury `JsonHelper`. Token a scope se čtou přímo uvnitř procedury `GetToken` označené `[NonDebuggable]`, token se ukládá do `SecretText`. Tato úprava je **už v pozdějším oficiálním zdroji 28.4**, takže ji neoznačujeme za novinku dostupnou výhradně od 28.5. Zdroj: [28.4 maintenance update z 2026-08-28 (#10688)](https://github.com/microsoft/BCApps/commit/8228410a).

---

*Části do 28.4 vycházejí z diffů větve `w1-28` (StefanMaron/MSDyn365BC.Code.History). Část 28.4 → 28.5 vychází z přímého diffu výše uvedených snapshotů microsoft/BCApps; rozdíl proti původnímu dokumentovanému buildu je popsán samostatně.*
