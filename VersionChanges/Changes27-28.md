# Shopify Connector - Změny mezi verzemi BC 27 a BC 28 (Changes 27-28)

Tento dokument detailně popisuje změny v **Shopify Connectoru** při přechodu z verze **Business Central 27** (w1-27.5) na verzi **Business Central 28** (w1-28.0).

---

## 📊 Základní statistika změn
* **Počet změněných souborů:** 233
* **Přidané řádky (Insertions):** 4 155
* **Smazané řádky (Deletions):** 1 128

---

## 🔑 Klíčové novinky a úpravy

### 1. 🛒 Kolekce produktů (Shopify Product Collections)
* **Nový koncept:** Konektor nyní plně podporuje správu a synchronizaci **kolekcí** z Shopify přímo v Business Central.
* **Přidané objekty:**
  * Tabulka: `Shpfy Product Collection` (ID 30143)
  * Tabulka: `Shpfy Shop Collection Map` (ID 30144)
  * Stránka: `Shpfy Product Collections` (ID 30143)
  * Codeunit: `Shpfy Product Collection API` (ID 30267) – řeší komunikaci s Shopify API pro kolekce.

### 2. 🖼️ Synchronizace obrázků u variant (Variant Images)
* **Nový koncept:** Přidána možnost exportovat a nastavovat obrázky specificky pro konkrétní produktové varianty.
* **Přidané objekty:**
  * Codeunit: `Shpfy Variant Image Export` (ID 30268)
  * GraphQL Codeunity: `Shpfy GQL Set VariantImage` (ID 30206), `Shpfy GQL GetVariantImage` (ID 30208)

### 3. 📦 Pokročilé objednávky na plnění (Fulfillment Orders)
* **Zpřesnění procesů:** Došlo k výraznému rozšíření struktury pro správu a synchronizaci fulfillment objednávek z Shopify (přechod na nový model Shopify Fulfillment Orders API).
* **Přidané objekty:**
  * Stránky: `Shpfy FulFillment Orders` (ID 30164), `Shpfy Fulfillment Order Card` (ID 30165)
  * Tabulky: `Shpfy FulFillment Order Header` (ID 30154), `Shpfy FulFillment Order Line` (ID 30155)

### 4. ↩️ Refaktorování vracení zboží (Returns & Refunds)
* **Změna architektury:** Microsoft kompletně přepsal a zjednodušil logiku zpracování vratek (Returns). Staré převodní objekty byly smazány a nahrazeny čistšími enumy.
* **Změny v objektech:**
  * Smazán codeunit: `Shpfy Return Enum Convertor` (ID 30142)
  * Přidán enum: `Shpfy Return Line Type` (ID 30132)
  * Přidána podpora pro refundaci nákladů na dopravu (Shipping Lines) v refundacích.
  * Stránky: `Shpfy Refund Lines` (ID 30161), `Shpfy Refund Shipping Lines` (ID 30162)
  * Tabulka: `Shpfy Refund Shipping Line` (ID 30139)

### 5. ⚙️ Mapování atributů zboží jako vlastností (Item Attributes)
* **Změna chování:** Nově lze ovlivnit, které atributy zboží z BC se mají přenášet a mapovat jako varianty/vlastnosti produktu do Shopify.
* **Přidané objekty:**
  * Tabulka (Rozšíření): `Shpfy Item Attribute` (ID 30103)
  * Stránka (Rozšíření): `Shpfy Item Attributes` (ID 30103)
  * Enum: `Shpfy Incl. in Product Sync` (ID 30133) – určuje, zda se atribut přenáší (např. *As Option*, *As HTML*, *Disabled*).

### 6. 🧠 Nový logovací engine a vynechané záznamy
* **Vylepšení:** Celá logika ukládání chyb a vynechaných záznamů byla vyčleněna do nového robustního codeunitu.
* **Přidané objekty:**
  * Codeunit: `Shpfy Log Entries` (ID 30272) – zajišťuje asynchronní a spolehlivé ukládání logů.

### 7. 💵 Měny (Currency Handling)
* **Vylepšení:** Přidán nový enum `Shpfy Currency Handling` (ID 30134) pro lepší nastavení přepočtů měn (např. *Local Currency*, *Shop Currency*).

---
*Dokument byl vygenerován lokálně pro větev `w1-28.0` na základě diffu s větví `w1-27.5`.*
