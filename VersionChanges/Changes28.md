# Shopify Connector - Změny v rámci verze BC 28 (Changes 28 - Minor Updates)

Tento dokument detailně popisuje změny a minoritní aktualizace v **Shopify Connectoru** v rámci verze **Business Central 28** (konkrétně přechod z verze **28.0** na verzi **28.1**).

---

## 📊 Základní statistika změn
* **Počet změněných souborů:** 23
* **Přidané řádky (Insertions):** 265
* **Smazané řádky (Deletions):** 29

---

## 🔑 Detaily změn v minor verzi 28.1

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
*Dokument byl vygenerován lokálně pro větev `w1-28.1` na základě diffu s větví `w1-28.0`.*
