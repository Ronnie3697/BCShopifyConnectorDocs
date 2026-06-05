# Shopify Connector - Funkční oblasti a procesy

Tento dokument vysvětluje hlavní procesní logiku a provázanost objektů v Shopify Connectoru.

## 🛒 1. Správa Zboží a Variant (Products & Variants)
* **Hlavní Codeunit:** [ShpfyCreateProduct.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Products/Codeunits/ShpfyCreateProduct.Codeunit.al)
  * Vytváří dočasné produkty a varianty a posílá je do Shopify přes API [ShpfyProductAPI.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Products/Codeunits/ShpfyProductAPI.Codeunit.al).
* **Exportní logika:** [ShpfyProductExport.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Products/Codeunits/ShpfyProductExport.Codeunit.al)
  * Zpracovává mapování atributů zboží na produktové varianty, kontroluje limity (max 3 vlastnosti) a validuje unikátnost variant.
* **Cenotvorba:** [ShpfyProductPriceCalc.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Products/Codeunits/ShpfyProductPriceCalc.Codeunit.al)
  * Provádí kalkulaci prodejních cen a porovnávacích cen pro export do Shopify.

## 👥 2. Synchronizace Zákazníků (Customers & Companies)
* **Zákazníci (B2C):** [ShpfyCustomerImport.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Customers/Codeunits/ShpfyCustomerImport.Codeunit.al) a [ShpfyCustomerMapping.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Customers/Codeunits/ShpfyCustomerMapping.Codeunit.al)
  * Řeší import a párování zákazníků na základě e-mailu nebo telefonního čísla.
* **Firmy (B2B):** [ShpfyCompanyImport.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Companies/Codeunits/ShpfyCompanyImport.Codeunit.al)
  * Import a zpracování B2B zákazníků a firemních účtů (Company) z Shopify.

## 📦 3. Objednávky a Plnění (Orders & Fulfillments)
* **Import objednávek:** [ShpfyOrderImport.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Order%20handling/Codeunits/ShpfyOrderImport.Codeunit.al) a [ShpfyOrdersEvents.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Order%20handling/Codeunits/ShpfyOrdersEvents.Codeunit.al)
  * Načítá objednávky přes GraphQL a převádí je na objednávky v BC.
* **Plnění (Fulfillments):** [ShpfySyncShipm.toShopify.Report.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Order%20Fulfillments/Reports/ShpfySyncShipm.toShopify.Report.al)
  * Odesílá informace o zaúčtovaných dodávkách zpět do Shopify pro aktualizaci stavu doručení objednávky.

## ⚠️ 4. Protokol vynechaných záznamů (Skipped Records)
* **Tabulka:** [ShpfySkippedRecord.Table.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Logs/Tables/ShpfySkippedRecord.Table.al)
* **Stránka:** [ShpfySkippedRecords.Page.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Logs/Pages/ShpfySkippedRecords.Page.al)
* **Codeunit:** [ShpfySkippedRecord.Codeunit.al](https://github.com/StefanMaron/MSDyn365BC.Code.History/blob/w1-28/Shopify/app/Shopify%20Connector/src/Logs/Codeunits/ShpfySkippedRecord.Codeunit.al)
  * Zajišťuje logování důvodů, proč systém při exportu vynechal určité zboží, varianty nebo zákazníky. Nabízí notifikace v uživatelském rozhraní a přímý proklik na vynechaný záznam.
