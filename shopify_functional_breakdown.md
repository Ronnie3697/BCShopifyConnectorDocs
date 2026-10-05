# Shopify Connector - Funkční oblasti a procesy

Tento dokument vysvětluje hlavní procesní logiku a provázanost objektů v Shopify Connectoru podle zdrojů **BC 29.0**. Podrobnosti novinek najdeš v [changelogu 28 ➔ 29](VersionChanges/Changes28-29.md).

## 🔌 0. Komunikace se Shopify (GraphQL a autentizace)
* **Volání API:** [ShpfyCommunicationMgt.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Base/Codeunits/ShpfyCommunicationMgt.Codeunit.al) (`Access = Internal`, Admin API verze 2026-07)
  * Posílá GraphQL dotazy, hlídá throttling přes [ShpfyGraphQLRateLimit.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/GraphQL/Codeunits/ShpfyGraphQLRateLimit.Codeunit.al) a při HTTP 401 jednou vynutí obnovu tokenu.
* **Texty dotazů:** od 29.0 v resource souborech [App/.resources/graphql/&lt;Oblast&gt;/&lt;Dotaz&gt;.graphql](https://github.com/microsoft/BCApps/tree/releases/29.0/src/Apps/W1/Shopify/App/.resources/graphql) (hlavička `# cost: N` + JSON). Načítá je [ShpfyGraphQLQueries.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/GraphQL/Codeunits/ShpfyGraphQLQueries.Codeunit.al) podle názvu hodnoty enumu `Shpfy GraphQL Type` ve tvaru `{Oblast}_{Dotaz}`. GQL codeunity a interface `Shpfy IGraphQL` zmizely.
* **Tokeny:** [ShpfyAuthenticationMgt.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Integration/Codeunits/ShpfyAuthenticationMgt.Codeunit.al) před každým voláním kontroluje platnost tokenu (`EnsureValidAccessToken`). Starý neexpirující token jednou vymění za expirující, expirující obnovuje refresh tokenem a po vypršení refresh tokenu nabídne **Reconnect**. Shopify neexpirující tokeny přestane od 2027-01-01 přijímat.

## 🛒 1. Správa Zboží a Variant (Products & Variants)
* **Hlavní Codeunit:** [ShpfyCreateProduct.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyCreateProduct.Codeunit.al)
  * Vytváří dočasné produkty a varianty a posílá je do Shopify přes API [ShpfyProductAPI.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProductAPI.Codeunit.al).
  * Zboží s více než 2048 variantami přeskočí a zapíše do Skipped Records (limit Shopify).
* **Exportní logika:** [ShpfyProductExport.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProductExport.Codeunit.al)
  * Zpracovává mapování atributů zboží na produktové varianty, kontroluje limity (max 3 vlastnosti) a validuje unikátnost variant.
  * Před vytvářením chybějících variant znovu načítá hlavní zboží produktu, aby po „Add Item as Shopify Variant“ nepřidával nenamapované varianty jiného zboží (od 28.5).
  * Při zapnutém `Sync HS Code and Country` posílá `Tariff No.` jako `harmonizedSystemCode` a `Country/Region of Origin Code` jako `countryCodeOfOrigin` (od 29.0).
* **Mapování:** [ShpfyProductMapping.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProductMapping.Codeunit.al) páruje varianty podle SKU. Hledání podle čárového kódu jako záložní varianta jde od 29.0 vypnout polem `Find Mapping by Barcode` na obchodu.
* **Public fasáda pro rozšíření:** [ShpfyProduct.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProduct.Codeunit.al) (30234) nabízí od 29.0 i `ConfirmAddItemToShopify`, `CheckItemAttributesCompatibleForProductOptions` a `GetProductUrl`.
* **Cenotvorba:** [ShpfyProductPriceCalc.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProductPriceCalc.Codeunit.al)
  * Provádí kalkulaci prodejních cen a porovnávacích cen pro export do Shopify.

## 👥 2. Synchronizace Zákazníků (Customers & Companies)
* **Zákazníci (B2C):** [ShpfyCustomerImport.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Customers/Codeunits/ShpfyCustomerImport.Codeunit.al) a [ShpfyCustomerMapping.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Customers/Codeunits/ShpfyCustomerMapping.Codeunit.al)
  * Řeší import a párování zákazníků na základě e-mailu nebo telefonního čísla.
  * [ShpfyCustomerAPI.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Customers/Codeunits/ShpfyCustomerAPI.Codeunit.al) přijme první výsledek hledání v Shopify pouze při přesné shodě e-mailu bez ohledu na velikost písmen nebo telefonu po odstranění oddělovačů (od 28.5). Předvolbu země nedoplňuje.
* **Firmy (B2B):** [ShpfyCompanyImport.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Companies/Codeunits/ShpfyCompanyImport.Codeunit.al)
  * Import a zpracování B2B zákazníků a firemních účtů (Company) z Shopify. Belgické firmy (`Enterprise No.`) řeší samostatné rozšíření Shopify Connector BE.

## 📦 3. Objednávky a Plnění (Orders & Fulfillments)
* **Import objednávek:** [ShpfyImportOrder.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Order%20handling/Codeunits/ShpfyImportOrder.Codeunit.al) a [ShpfyOrderEvents.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Order%20handling/Codeunits/ShpfyOrderEvents.Codeunit.al)
  * Načítá objednávky přes GraphQL a převádí je na objednávky v BC. Od 29.0 ukládá i `Tax Area Code`, `Tax Liable` a `Tax Exempt` a označuje vyměněné položky (`Is Exchange Item`).
* **Mapování a vytvoření dokladu:** [ShpfyOrderMapping.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Order%20handling/Codeunits/ShpfyOrderMapping.Codeunit.al) (po mapování nový event `OnAfterMapShopifyOrder`) a [ShpfyProcessOrder.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Order%20handling/Codeunits/ShpfyProcessOrder.Codeunit.al)
  * Při `Use Shopify Order No.` dostane prodejní objednávka nebo faktura číslo Shopify objednávky (od 29.0).
* **Plnění (Fulfillments):** [ShpfySyncShipmToShopify.Report.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Shipping/Reports/ShpfySyncShipmToShopify.Report.al)
  * Odesílá informace o zaúčtovaných dodávkách zpět do Shopify pro aktualizaci stavu doručení objednávky. Od 29.0 rozdělí dodávku přes více Shopify lokací do samostatných požadavků po lokacích.
* **Vratky a refundy:** [ShpfyRetRefProcCrMemo.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Order%20Return%20Refund%20Processing/Codeunits/ShpfyRetRefProcCrMemo.Codeunit.al)
  * Typ zpracování *Auto Create Sales Document* založí podle pole obchodu `Process Returns As` dobropis nebo vratkovou objednávku (od 29.0).

## 📊 4. Synchronizace skladu (Inventory)
* **Spuštění:** [ShpfySyncStockToShopify.Report.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Inventory/Reports/ShpfySyncStockToShopify.Report.al) má od 29.0 volby **Skip Import Stock** a **Variant ID Filter**.
* **Výpočet a export:** [ShpfyInventoryAPI.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Inventory/Codeunits/ShpfyInventoryAPI.Codeunit.al) posílá změněné stavy. Se `Skip Import Stock` posílá i stavy, které se od uloženého `Shopify Stock` neliší, protože ten nebyl čerstvě načten.

## ⚠️ 5. Protokol vynechaných záznamů (Skipped Records)
* **Tabulka:** [ShpfySkippedRecord.Table.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Logs/Tables/ShpfySkippedRecord.Table.al)
* **Stránka:** [ShpfySkippedRecords.Page.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Logs/Pages/ShpfySkippedRecords.Page.al)
* **Codeunit:** [ShpfySkippedRecord.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Logs/Codeunits/ShpfySkippedRecord.Codeunit.al)
  * Zajišťuje logování důvodů, proč systém při exportu vynechal určité zboží, varianty nebo zákazníky. Nabízí notifikace v uživatelském rozhraní a přímý proklik na vynechaný záznam. Od 29.0 má dlaždici na stránce Activities (vedle dlaždice API Errors).

## 💰 6. Synchronizace cen katalogů (Catalog Prices)

* **Spuštění a filtry:** [ShpfySyncCatalogPrices.Report.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Catalogs/Reports/ShpfySyncCatalogPrices.Report.al) od 28.5 umožňuje omezit katalogy podle **Id** a **Name**. Rozsáhlou synchronizaci tak lze rozdělit do menších dávek; zpracovávají se katalogy s povoleným `Sync Prices`.
* **Zpracování katalogu:** [ShpfySyncCatalogPrices.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/29.0/src/Apps/W1/Shopify/App/src/Catalogs/Codeunits/ShpfySyncCatalogPrices.Codeunit.al) nastaví kontext obchodu a katalogu pro výpočet cen a synchronizuje ceny. V rámci jednoho nastavení obchodu přeskočí již zpracovaná ID katalogů.
