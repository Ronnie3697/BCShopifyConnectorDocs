# Shopify Connector - Změny v rámci verze BC 29 (Changes 29 - Minor Updates)

Tento dokument bude popisovat minoritní aktualizace **Shopify Connectoru** v rámci verze **Business Central 29** (29.0 ➔ 29.1 ➔ …). Přechod z BC 28 popisuje [Changes28-29.md](Changes28-29.md).

---

## Výchozí bod: BC 29.0

* **Zdroj:** [microsoft/BCApps, `releases/29.0`](https://github.com/microsoft/BCApps/tree/releases/29.0/src/Apps/W1/Shopify), verze v `App/app.json` **29.0.0.0**.
* **Snapshot:** [`84f94fce`](https://github.com/microsoft/BCApps/commit/84f94fce9754c8d1c9440dc62885ff33788778ae) (2026-10-05), **509 AL objektů**.
* Další minor verzi porovnávej přímým diffem proti tomuto snapshotu:
  `git diff --stat 84f94fce9754c8d1c9440dc62885ff33788778ae <sha-nové-verze> -- src/Apps/W1/Shopify`

---

## Servisní opravy v `releases/29.0` (bez změny verze 29.0.0.0)

Snapshot ke 2026-10-19: [`28896630`](https://github.com/microsoft/BCApps/commit/288966302f7be8f3fe08f02cde0059a4c4a7f4a7). Počet objektů beze změny (509).

### Daně objednávek mimo US/CA ([#12436](https://github.com/microsoft/BCApps/commit/201336cdb45b2dadef363402020f13c1dd096878), 2026-10-08)

* Backport #11722 a #11899: párování daní Shopify objednávek (Shopify Tax Matching) se **nespouští pro objednávky mimo USA a Kanadu**.
* Jediná změna v App proti snapshotu 29.0: `Shpfy Order Tax Line` (30122), pole `Title` prodlouženo z `Code[20]` na **`Code[100]`** (s `#pragma warning disable AS0086`, tabulka je internal). Delší názvy daní ze Shopify už nepadají na délce pole.
* Zbytek commitu jsou testy (`ShpfyShippingChargesTest`).

---

*Průběžná větev `releases/29.x` není číselná release větev a `update_docs.py --check-latest` ji ignoruje.*
