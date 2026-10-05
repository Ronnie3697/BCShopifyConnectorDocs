# Shopify Connector - Změny mezi verzemi BC 28 a BC 29 (Changes 28-29)

Tento dokument popisuje změny v **Shopify Connectoru** při přechodu z verze **Business Central 28** (`releases/28.5`) na verzi **Business Central 29** (`releases/29.0`) v oficiálním repozitáři [microsoft/BCApps](https://github.com/microsoft/BCApps/tree/releases/29.0/src/Apps/W1/Shopify).

Ověřeno 2026-10-05 přímým diffem zdrojů. Verze v `App/app.json` je **29.0.0.0** (`platform` i `application` 29.0.0.0). Není to číslo konkrétního distribuovaného buildu ani potvrzení dostupnosti aktualizace v tenantech.

---

## 📊 Základní statistika změn

* **Porovnávané snapshoty:** 28.5 [`45d68f32`](https://github.com/microsoft/BCApps/commit/45d68f32077c89de4b422a8c05cc8f88959bba18) ➔ 29.0 [`84f94fce`](https://github.com/microsoft/BCApps/commit/84f94fce9754c8d1c9440dc62885ff33788778ae) (přímý `git diff`; webový compare ukazuje rozdíl od společného předka).
* **Celá složka Shopify:** 539 změněných souborů, +12 928 / −7 937 řádků (včetně testů, `.graphql` resource souborů a nové in-repo dokumentace).
* **Produkční AL kód (`App/src/*.al`):** 268 souborů (1 přidaný, 131 smazaných, 136 upravených), +3 463 / −5 391 řádků.
* **Počet AL objektů:** **639 ➔ 509**. Zmizelo 129 GQL codeunitů, codeunit `Shpfy Communication Events` a interface `Shpfy IGraphQL`; přibyl codeunit `Shpfy CreateProdStatusUnlisted` (30205).
* Do 28.x už dřív backportované změny (filtry katalogů, párování zákazníků podle telefonu, `Shpfy Update Price Source` public, pending refund transakce…) v tomto diffu nejsou — popisuje je [Changes28.md](Changes28.md).

---

## ⚠️ Co musí řešit vývojáři rozšíření a provoz

### 1. 🔐 Expirující offline access tokeny — termín 2027-01-01
* **Proč:** Shopify od **2027-01-01** odmítne Admin API volání s neexpirujícími offline tokeny (týká se veřejných appek založených před 2026-04-01). Konektor proto přechází na **expirující tokeny s rotací refresh tokenu** (access token platí 1 hodinu, refresh token 90 dní).
* **Jak to funguje:** `Shpfy Authentication Mgt.` (30199) má nový orchestrátor `EnsureValidAccessToken`, volaný z `Shpfy Communication Mgt.GetAccessToken` před každým API voláním (interaktivním i na pozadí). Starý neexpirující token se při prvním použití jednorázově a nevratně vymění za expirující (při neúspěchu se opakuje nejvýš jednou za hodinu, starý token zůstává platný); expirující token se před vypršením obnoví. Při HTTP 401 se vynutí obnova nejvýš jednou za minutu.
* **Nová pole** v `Shpfy Registered Store New` (30138): `Token Expires At` (6), `Refresh Token Expires At` (7), `Last Migration Attempt` (8), `Last Force Refresh At` (9); refresh token se ukládá jako `SecretText`.
* **Když refresh token propadne** (90 dní bez synchronizace nebo odebraný přístup v Shopify): karta obchodu ukáže notifikaci s akcí **Reconnect** a API volání skončí chybou s akcí pro nové přihlášení.
* ⚠️ **BC 28:** k 2026-10-02 tahle migrace **není** ve větvi `releases/28.x` (28.6.0.0). Tenanty, které do 2027-01-01 zůstanou na BC 28 bez backportu, přijdou o spojení se Shopify. Sledujte případný backport do 28.x.
* Zdroj: [#9327](https://github.com/microsoft/BCApps/commit/9c922717).

### 2. 🧩 GraphQL dotazy v resource souborech místo codeunitů
* **Změna architektury:** 143 codeunitů `Shpfy GQL *`, které jen vracely text dotazu a cenu, nahradilo **149 souborů `App/.resources/graphql/<Oblast>/<Dotaz>.graphql`**. Každý soubor má hlavičku `# cost: N` a JSON tělo dotazu; načítá je `Shpfy GraphQL Queries.GetQueryWithCost` (30154) přes `NavApp.GetResourceAsText`.
* **Enum `Shpfy GraphQL Type` (30111):** hodnoty jsou přejmenované na `{Oblast}_{Dotaz}` (např. `GetCustomerIds` ➔ `Customers_GetCustomerIds`), ordinální čísla zůstala. Enum už neimplementuje interface a změnil se z `Extensible = true` na **`Extensible = false`**. Enum byl a je `Access = Internal`.
* **Smazáno:** interface `Shpfy IGraphQL`, 129 GQL codeunitů (ID 30100–30455) a interní eventy `OnBeforeSetInterfaceCodeunit`, `OnBeforeGetGrapQLInfo`, `OnAfterGetGrapQLInfo`, `OnBeforeReplaceParameters` a `OnAfterReplaceParameters` v `Shpfy GraphQL Queries`.
* **Zbylo 14 GQL codeunitů** (např. `Shpfy GQL RefundLines`, `Shpfy GQL ModifyInventory`) jako `ObsoleteState = Pending` obaly pod `#if not CLEAN29`; jejich `GetGraphQL` / `GetExpectedCost` jsou nově public a jen volají `GetQueryWithCost`.
* **Dopad:** rozšíření, která odkazovala na smazané codeunity (v permission setech, přes `Codeunit::"Shpfy GQL …"`) nebo na původní názvy hodnot enumu, se na 29 nezkompilují.
* Zdroj: [#7198](https://github.com/microsoft/BCApps/commit/d2e54221).

### 3. 🧪 Testovací mocking přes `HttpClientHandler`
* Smazán codeunit **`Shpfy Communication Events` (30200)** s interními eventy `OnClientSend`, `OnClientPost`, `OnClientGet`, `OnGetContent` a `OnGetAccessToken`. Z `Shpfy Communication Mgt.` (30103) zmizely `SetTestInProgress` / `GetTestInProgress` a všechny větve `if IsTestInProgress`.
* Z `Shpfy Product API` zmizel interní event `OnBeforeUploadImage`.
* Testy konektoru teď používají platformní `[HttpClientHandler]` s `TestHttpRequestPolicy = BlockOutboundRequests`. Vlastní testy rozšíření, které mockovaly HTTP přes zmíněné eventy, je nutné přepsat stejně.
* Zdroj: [#7204](https://github.com/microsoft/BCApps/commit/38dbba44).

### 4. 🌐 Shopify Admin API 2026-07 a doprava řízená trhy
* `VersionTok` v `Shpfy Communication Mgt.` (30103): **2026-01 ➔ 2026-07**.
* `Shpfy Shipping Methods` (30193) rozpozná obchody s **market-driven shipping** (`ShopFeatures.marketDrivenShipping`; Shopify je zavádí od 2026-10-01, pro všechny obchody do 2027-07-01). U nich čte názvy dopravních metod z `markets → delivery.shipping.optionDefinitions`; starý dotaz na `deliveryProfiles` by vracel neúplná data a rozbil `Shpfy Shipment Method Mapping`. Nové dotazy: `Shipping_GetMarketShippingMethods`, `Shipping_GetNextMarketShippingMethods`.
* Zdroj: [#9221](https://github.com/microsoft/BCApps/commit/108e78e5).

### 5. ⏱️ Omezování rychlosti GraphQL volání
* Volání přes `ExecuteGraphQL(GraphQLQuery: Text)` (create/update zákazníků, firem, produktů, variant, draft objednávek, fulfillmentů) dřív posílala `ExpectedCost = 0`. Rate limiter je tak vůbec nebrzdil a na malých obchodech (např. vývojových) docházelo k neustálému throttlingu. Nově se tato volání také zpomalují ([#10417](https://github.com/microsoft/BCApps/commit/19796c4e)).
* Opraveno i nedostatečné čekání limiteru po uplynulém čase ([#9146](https://github.com/microsoft/BCApps/commit/fceda696)).

---

## 🔑 Nové funkce

### 6. 🔢 Číslo Shopify objednávky jako číslo dokladu
* **Nové pole** `Use Shopify Order No.` na `Shpfy Shop` (30102, pole 136) a na `Shpfy Order Header` (30118, pole 135). Na objednávce jde nastavení přepsat jednotlivě.
* Prodejní objednávka nebo faktura pak dostane `No.` = `Shopify Order No.`. Číslo začínající `@` skončí chybou. Karta obchodu při zapnutí upozorní, pokud číselné řady objednávek (případně faktur) nemají povolené `Manual Nos.`
* Zdroj: [#6721](https://github.com/microsoft/BCApps/commit/2f452a09).

### 7. ↩️ Vratky jako dobropis nebo vratková objednávka
* **Nové pole** `Process Returns As` na `Shpfy Shop` (pole 137, enum `Sales Document Type`, povolené jen `Credit Memo` / `Return Order`, výchozí `Credit Memo`).
* Hodnota `Auto Create Credit Memo` enumu `Shpfy ReturnRefund ProcessType` (30139) má nově caption **Auto Create Sales Document** (název hodnoty zůstal). Podle nového pole založí dobropis nebo vratkovou objednávku (`Shpfy RetRefProc Cr.Memo`, 30243).
* Zdroj: [#6722](https://github.com/microsoft/BCApps/commit/d67fba96).

### 8. 🌍 Celní sazebník (HS kód) a země původu
* **Nové pole** `Sync HS Code and Country` na `Shpfy Shop` (pole 209, caption *Sync HS Code and Country of Origin*, **výchozí zapnuto**). Na `Shpfy Variant` (30129) přibyla pole `Tariff No.` (109) a `Country/Region of Origin Code` (110).
* **Export:** `Item."Tariff No."` jde do Shopify jako `harmonizedSystemCode`, `Item."Country/Region of Origin Code"` jako `countryCodeOfOrigin`.
* **Import** (jen při zapnutém nastavení): při zakládání a aktualizaci zboží se doplní obě pole. Celní sazba se přiřadí jen tehdy, když už v BC existuje; Shopify vrací kód bez oddělovačů, proto se porovnávají číslice. Nová celní sazba se nezakládá.
* Zdroj: [#7414](https://github.com/microsoft/BCApps/commit/03134346), [#9320](https://github.com/microsoft/BCApps/commit/d03f4ddf).

### 9. 🏷️ Stav produktu Unlisted
* Enum `Shpfy Product Status` (30130) má novou hodnotu `Unlisted` (3). Import ji dřív neuměl převést a potichu z ní udělal `Active`.
* Enum `Shpfy Cr. Prod. Status Value` (30129) má hodnotu `Unlisted` (2) s implementací v novém codeunitu `Shpfy CreateProdStatusUnlisted` (30205). Nově vytvářené produkty tak mohou v Shopify vznikat jako skryté (dostupné jen přes přímý odkaz).
* Zdroj: [#9321](https://github.com/microsoft/BCApps/commit/41427447), [#9581](https://github.com/microsoft/BCApps/commit/03bf5578).

### 10. 📦 Řízení synchronizace skladu
* Report `Shpfy Sync Stock to Shopify` (30102) má request page s volbami **Skip Import Stock** a **Variant ID Filter**.
* Se `Skip Import Stock` se před exportem nenačítá stav skladu ze Shopify. Export pak posílá množství i u řádků, kde se `Stock` rovná uloženému `Shopify Stock`, protože tato hodnota může být neaktuální. Hodí se pro export po zaúčtování v BC bez zdlouhavého plného importu (u velkých katalogů i několik hodin).
* Zdroj: [#6396](https://github.com/microsoft/BCApps/commit/0b6f0057).

### 11. 🧾 Daňové údaje objednávek a dopravy
* `Shpfy Order Header` (30118) ukládá `Tax Area Code` (1070), `Tax Liable` (1080) a `Tax Exempt` (1090), stejně tak `Shpfy Refund Header` (30142, pole 110–112). Hodnoty se předají do Sales Header při vytváření objednávky i dobropisu; když je kód prázdný, použije se dohledání přes `FindTaxArea`.
* **Nový event** `OnAfterMapShopifyOrder(var ShopifyOrderHeader; Result)` v `Shpfy Order Events` (30162), s `CommitBehavior::Ignore`. Spouští se po mapování zákazníka, zboží, dopravy, platby a daňové oblasti.
* Daňové řádky dopravy se ukládají do `Shpfy Order Tax Line` (30122) s vazbou na dopravní řádek. Stránka `Shpfy Order Shipping Charges` (30128) má akci **Tax Lines** ([#9537](https://github.com/microsoft/BCApps/commit/bb8504c5)).
* Zdroj: [#10407](https://github.com/microsoft/BCApps/commit/ec7ec56b).

### 12. 🔁 Výměny zboží (exchanges)
* Nové pole `Is Exchange Item` na `Shpfy Order Line` (30119, pole 22) a `Shpfy Refund Line` (30145, pole 14), zobrazené na podstránkách.
* Opravy dobropisů u výměn: chybný řádek finančního účtu ([#8554](https://github.com/microsoft/BCApps/commit/3239a62f)), výměna za dražší zboží bez vyrovnávacího řádku a falešné varování o zpracované objednávce ([#10467](https://github.com/microsoft/BCApps/commit/11884afa)), odkazy, součty a rozložení stránky refundu ([#11401](https://github.com/microsoft/BCApps/commit/809cc338)). Doklad vytvořený z dobropisu výměny přes Copy Document s volbou *Move Negative Lines* se naváže na Shopify objednávku (`Shpfy Copy Sales Document`).

### 13. 🛒 Export produktů a mapování
* **Barcode fallback lze vypnout:** nové pole `Find Mapping by Barcode` na `Shpfy Shop` (pole 208, výchozí zapnuto, na kartě obchodu skryté). Vypnutím se při nenalezené shodě podle SKU nehledá podle čárového kódu ([#7692](https://github.com/microsoft/BCApps/commit/c663fd51)).
* **Limit 2048 variant:** zboží s více variantami se při exportu přeskočí a zapíše do Skipped Records. Dřív `productVariantsBulkCreate` potichu selhal ([#7113](https://github.com/microsoft/BCApps/commit/78853f82)).
* **Kontrola před Add to Shopify:** blokované zboží nebo zboží bez popisu se zapíše do Skipped Records ([#7361](https://github.com/microsoft/BCApps/commit/30251e3a)).
* **Fulfillment podle lokací:** dodávka přes více Shopify lokací se odešle jako samostatné `fulfillmentCreate` mutace po lokacích. Dřív končila chybou *All fulfillment orders must be assigned to a single location*. Přibyl klíč na `Shpfy FulFillment Order Line` (30144) ([#7065](https://github.com/microsoft/BCApps/commit/e98ea20e)).

### 14. 🧱 Nové public API pro rozšíření
* `Shpfy Product` (30234): `ConfirmAddItemToShopify`, `CheckItemAttributesCompatibleForProductOptions` a `GetProductUrl`. Partner tak může zopakovat stejný postup jako akce **Add to Shopify** na kartě zboží ([#8713](https://github.com/microsoft/BCApps/commit/9436d2e1)).
* Stránka `Shpfy Add Item Confirm` (30144): `SetShopCode`, `SetItemDescription` a `SetIsActive` jsou nově public ([#8871](https://github.com/microsoft/BCApps/commit/aba239d5)).
* Pozor: `Shpfy Communication Mgt.`, `Shpfy Authentication Mgt.`, enum `Shpfy GraphQL Type` i pole `Shopify URL` na `Shpfy Shop` zůstávají `Access = Internal`.

### 15. 🖥️ Uživatelské rozhraní
* **Activities:** dlaždice `Skipped Records` a `API Errors` (`Shpfy Cue` 30100, pole 10 a 11) ([#10092](https://github.com/microsoft/BCApps/commit/7ab5ae2f)).
* **Navigace:** stránka Companies v Role Center rozšířeních Business Manager, Order Processor a Sales Relationship Manager.
* **Varianty:** pole `Compare-at Price` na stránce `Shpfy Variants` (30127), k dispozici pro personalizaci.
* **Objednávka** (`Shpfy Order`, 30113): editovatelná pole Sell-to, Bill-to a Ship-to `Contact No.` s lookupem na kontakty zákazníka, daňová pole a `Use Shopify Order No.`
* **Transakce:** pole `Shpfy Order No.` na `Shpfy Order Transaction` (30133, pole 109) a na stránkách transakcí. Refund má skupinu Tax a akce **Tax Lines** a **Transactions**.
* **Log Entries:** pohled *With errors*. **Bulk Operations:** odeslaný JSONL (`Sent JSONL`, pole 13) a akce **Get Sent Data** ([#9211](https://github.com/microsoft/BCApps/commit/9517d4e6)).
* **Karta obchodu:** nový záznam v sandboxu nebo demo společnosti má vypnuté `Allow Background Syncs`. Obchod nejde uložit s prázdným kódem. ToolTipy se přesunuly ze stránky do tabulky. Přejmenované captiony: `Auto Create Orders` ➔ *Auto Create Sales Documents*, `Auto Release Sales Orders` ➔ *Auto Release Sales Documents*, `Customer Template Code` ➔ *Customer/Company Template Code*, `Return and Refund Process` ➔ *Process Type*, `Allow Outgoing Requests` ➔ *Allow Data Sync to Shopify*, `Order Created Webhooks` ➔ *Auto Sync Orders*, `Order Created Webhook User` ➔ *Sync Order Job Queue User*.
* **Výchozí hodnota:** `Allow Line Disc.` (pole 61) má nově `InitValue = true` ([#7576](https://github.com/microsoft/BCApps/commit/4d872f91)).

### 16. 🌐 Lokalizační rozšíření (mimo W1 konektor)
* **Shopify Connector BE** (`src/Apps/BE/ShopifyBE`): mapování daňového ID belgických firem na `Enterprise No.` (rozšiřuje enum `Shpfy Comp. Tax Id Mapping`, 30166) ([#9138](https://github.com/microsoft/BCApps/commit/2df6b409)).
* **Shopify Connector NA** (`src/Apps/NA/ShopifyNA`): Copilot **Tax Matching Agent**, který pomocí AI páruje Shopify daňové řádky s daňovými jurisdikcemi BC ([#10724](https://github.com/microsoft/BCApps/commit/a7dcd566)). W1 konektor mu přidal `internalsVisibleTo`.
* `Shpfy Shop Mgt.` (30211) v aplikační rodině BE, respektive US (CA/MX zatím ne) nabídne instalaci příslušného rozšíření notifikací s akcí **Install**.

### 17. 🛠️ Vybrané opravy
* Synchronizace produktů už nemaže namapované varianty kvůli zastaralému `Updated At` ([#9313](https://github.com/microsoft/BCApps/commit/210794a7)).
* Synchronizace cen nepoužívá zastaralé `WorkDate` ze SingleInstance cache ([#9404](https://github.com/microsoft/BCApps/commit/e286ff6c)). Práh pro bulk aktualizaci cen se počítá z počtu skutečně změněných cen ([#9126](https://github.com/microsoft/BCApps/commit/237399c6)).
* Import objednávky založí zákazníka i bez výchozí adresy v Shopify ([#9188](https://github.com/microsoft/BCApps/commit/ebe25d8f)). Ručně zadané `Sell-to Customer No.` se zachová, když selže mapování Bill-to ([#9316](https://github.com/microsoft/BCApps/commit/20deff8d)).
* Úprava objednávky (order edit): slevy odebraného množství ([#10462](https://github.com/microsoft/BCApps/commit/5eee885d)) a `Total Amount` po vrácení daně ([#7447](https://github.com/microsoft/BCApps/commit/31054b66)).
* Factbox Order Totals neotvírá cizí prodejní objednávku u navázané účtované faktury ([#10307](https://github.com/microsoft/BCApps/commit/1c10bca2)). Stránka Shops funguje i bez oprávnění k extensionům ([#10034](https://github.com/microsoft/BCApps/commit/a4f9b017)).
* Řádky objednávky se načítají po 10 místo po 3 ([#8545](https://github.com/microsoft/BCApps/commit/0bf980bc)). Tax Area při exportu zákazníka nebo firmy se filtruje podle ISO kódu země ([#8072](https://github.com/microsoft/BCApps/commit/9b52b6e4)).
* Upgrade přejmenuje italské provincie Olbia-Tempio ➔ *Gallura Nord-Est Sardegna* a Carbonia-Iglesias ➔ *Sulcis Iglesiente* v `Shpfy Tax Area` ([#8546](https://github.com/microsoft/BCApps/commit/d083f4b9)).

---

## 📚 Nová in-repo dokumentace od Microsoftu

V `App/` přibyly `CLAUDE.md` a `docs/` (`business-logic.md`, `data-model.md`, `extensibility.md`, `patterns.md`) a v jednotlivých oblastech `src/<Oblast>/docs/CLAUDE.md`, případně `extensibility.md` ([#7283](https://github.com/microsoft/BCApps/commit/e10622c3), [#9812](https://github.com/microsoft/BCApps/commit/57bfb641)). Dobrý zdroj, když hledáš eventy a body rozšíření: [App/docs na releases/29.0](https://github.com/microsoft/BCApps/tree/releases/29.0/src/Apps/W1/Shopify/App/docs).

---

*Dokument vychází z přímého diffu snapshotů microsoft/BCApps `releases/28.5` (`45d68f32`) a `releases/29.0` (`84f94fce`) ve složce `src/Apps/W1/Shopify`, doplněného popisy PR. Testy byly čteny, nebyly spouštěny v BC.*
