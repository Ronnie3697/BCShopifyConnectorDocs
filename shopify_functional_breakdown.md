# Shopify Connector - Funkční oblasti a procesy

Tento dokument vysvětluje hlavní procesní logiku a provázanost objektů v Shopify Connectoru podle zdrojů **BC 28.5**. Podrobnosti novinek najdeš v [changelogu](VersionChanges/Changes28.md#bc-284--bc-285).

## 🛒 1. Správa Zboží a Variant (Products & Variants)
* **Hlavní Codeunit:** [ShpfyCreateProduct.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyCreateProduct.Codeunit.al)
  * Vytváří dočasné produkty a varianty a posílá je do Shopify přes API [ShpfyProductAPI.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProductAPI.Codeunit.al).
* **Exportní logika:** [ShpfyProductExport.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProductExport.Codeunit.al)
  * Zpracovává mapování atributů zboží na produktové varianty, kontroluje limity (max 3 vlastnosti) a validuje unikátnost variant.
  * V 28.5 před vytvářením chybějících variant znovu načítá hlavní zboží produktu, aby po „Add Item as Shopify Variant“ nepřidával nenamapované varianty jiného zboží.
* **Cenotvorba:** [ShpfyProductPriceCalc.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Products/Codeunits/ShpfyProductPriceCalc.Codeunit.al)
  * Provádí kalkulaci prodejních cen a porovnávacích cen pro export do Shopify.

## 👥 2. Synchronizace Zákazníků (Customers & Companies)
* **Zákazníci (B2C):** [ShpfyCustomerImport.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Customers/Codeunits/ShpfyCustomerImport.Codeunit.al) a [ShpfyCustomerMapping.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Customers/Codeunits/ShpfyCustomerMapping.Codeunit.al)
  * Řeší import a párování zákazníků na základě e-mailu nebo telefonního čísla.
  * [ShpfyCustomerAPI.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Customers/Codeunits/ShpfyCustomerAPI.Codeunit.al) v 28.5 přijme první výsledek hledání v Shopify pouze při přesné shodě e-mailu bez ohledu na velikost písmen nebo telefonu po odstranění oddělovačů. Předvolbu země nedoplňuje.
* **Firmy (B2B):** [ShpfyCompanyImport.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Companies/Codeunits/ShpfyCompanyImport.Codeunit.al)
  * Import a zpracování B2B zákazníků a firemních účtů (Company) z Shopify.

## 📦 3. Objednávky a Plnění (Orders & Fulfillments)
* **Import objednávek:** [ShpfyImportOrder.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Order%20handling/Codeunits/ShpfyImportOrder.Codeunit.al) a [ShpfyOrderEvents.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Order%20handling/Codeunits/ShpfyOrderEvents.Codeunit.al)
  * Načítá objednávky přes GraphQL a převádí je na objednávky v BC.
* **Plnění (Fulfillments):** [ShpfySyncShipmToShopify.Report.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Shipping/Reports/ShpfySyncShipmToShopify.Report.al)
  * Odesílá informace o zaúčtovaných dodávkách zpět do Shopify pro aktualizaci stavu doručení objednávky.

## ⚠️ 4. Protokol vynechaných záznamů (Skipped Records)
* **Tabulka:** [ShpfySkippedRecord.Table.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Logs/Tables/ShpfySkippedRecord.Table.al)
* **Stránka:** [ShpfySkippedRecords.Page.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Logs/Pages/ShpfySkippedRecords.Page.al)
* **Codeunit:** [ShpfySkippedRecord.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Logs/Codeunits/ShpfySkippedRecord.Codeunit.al)
  * Zajišťuje logování důvodů, proč systém při exportu vynechal určité zboží, varianty nebo zákazníky. Nabízí notifikace v uživatelském rozhraní a přímý proklik na vynechaný záznam.

## 💰 5. Synchronizace cen katalogů (Catalog Prices)

* **Spuštění a filtry:** [ShpfySyncCatalogPrices.Report.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Catalogs/Reports/ShpfySyncCatalogPrices.Report.al) od 28.5 umožňuje omezit katalogy podle **Id** a **Name**. Rozsáhlou synchronizaci tak lze rozdělit do menších dávek; zpracovávají se katalogy s povoleným `Sync Prices`.
* **Zpracování katalogu:** [ShpfySyncCatalogPrices.Codeunit.al](https://github.com/microsoft/BCApps/blob/releases/28.5/src/Apps/W1/Shopify/App/src/Catalogs/Codeunits/ShpfySyncCatalogPrices.Codeunit.al) nastaví kontext obchodu a katalogu pro výpočet cen a synchronizuje ceny. V rámci jednoho nastavení obchodu přeskočí již zpracovaná ID katalogů.
