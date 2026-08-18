#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generátor dokumentace Shopify Connectoru pro Business Central.

Projde AL zdrojáky ve sparse-checkoutu repa StefanMaron/MSDyn365BC.Code.History
(složka `Shopify/app/Shopify Connector/src`) a vygeneruje markdown soubory
shopify_tables.md, shopify_pages.md, shopify_codeunits.md a shopify_reports.md.

Sloupec "Popis / Summary" je konkatenace všech XML doc `<summary>` bloků
v souboru (whitespace sbalený, spojeno mezerou); bez doc komentářů je "-".

Použití:
    python parse_al.py --src <cesta ke checkoutu> --out <cesta k docs repu> [--branch w1-28]
"""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import quote

OBJ_RE = re.compile(
    r'^\s*(table|tableextension|page|pageextension|codeunit|report|reportextension'
    r'|enum|enumextension|interface|permissionset|permissionsetextension|query'
    r'|entitlement|profile|controladdin)\s+(?:(\d+)\s+)?("([^"]+)"|\w+)'
    r'(?:\s+extends\s+("([^"]+)"|\w+))?',
    re.IGNORECASE,
)
SUMMARY_RE = re.compile(r'<summary>(.*?)</summary>', re.DOTALL)

GITHUB_BASE = 'https://github.com/StefanMaron/MSDyn365BC.Code.History/blob'
APP_SRC = Path('Shopify') / 'app' / 'Shopify Connector' / 'src'


def parse_al_file(path: Path):
    """Vrátí (typ, id, název, extends, summary) prvního objektu v souboru."""
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    obj = None
    for line in text.splitlines():
        m = OBJ_RE.match(line)
        if m:
            name = m.group(4) if m.group(4) is not None else m.group(3)
            extends = m.group(6) if m.group(6) is not None else m.group(5)
            obj = {
                'type': m.group(1).lower(),
                'id': int(m.group(2)) if m.group(2) else None,
                'name': name,
                'extends': extends,
            }
            break
    if obj is None:
        return None

    doc_lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith('///'):
            doc_lines.append(stripped[3:])
    doc_text = '\n'.join(doc_lines)
    summaries = [' '.join(s.split()) for s in SUMMARY_RE.findall(doc_text)]
    summary = ' '.join(s for s in summaries if s).strip()
    obj['summary'] = summary if summary else '-'
    return obj


def collect_objects(src_root: Path, branch: str):
    objects = []
    src_dir = src_root / APP_SRC
    if not src_dir.is_dir():
        sys.exit(f'Nenalezena složka zdrojáků: {src_dir}')
    for path in sorted(src_dir.rglob('*.al')):
        obj = parse_al_file(path)
        if obj is None:
            print(f'VAROVÁNÍ: nerozpoznán objekt v {path}', file=sys.stderr)
            continue
        rel = path.relative_to(src_root).as_posix()
        obj['url'] = f'{GITHUB_BASE}/{branch}/{quote(rel, safe="/")}'
        obj['filename'] = path.name
        objects.append(obj)
    return objects


def md_row(obj, with_extends: bool) -> str:
    name = f'**{obj["name"]}**'
    if with_extends and obj.get('extends'):
        name += f' (extends {obj["extends"]})'
    obj_id = obj['id'] if obj['id'] is not None else ''
    summary = obj['summary'].replace('|', '\\|')
    return f'| {obj_id} | {name} | {summary} | [{obj["filename"]}]({obj["url"]}) |'


def md_section(title: str, objs, with_extends: bool) -> list:
    lines = [f'## {title} ({len(objs)})', '']
    lines.append('| ID | Název objektu | Popis / Summary | Zdrojový kód |')
    lines.append('| :--- | :--- | :--- | :--- |')
    for obj in sorted(objs, key=lambda o: (o['id'] is None, o['id'] or 0, o['name'])):
        lines.append(md_row(obj, with_extends))
    return lines


def write_md(path: Path, title: str, sections) -> None:
    lines = [f'# Shopify Connector - {title}', '',
             'Zde je seznam a přehled objektů v Shopify Connectoru.', '']
    first = True
    for section_title, objs, with_extends in sections:
        if not objs and not first:
            continue
        if not first:
            lines.append('')
        lines.extend(md_section(section_title, objs, with_extends))
        first = False
    lines.append('')
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'Zapsáno: {path}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--src', required=True, help='Root sparse-checkoutu (obsahuje složku Shopify/)')
    parser.add_argument('--out', required=True, help='Root docs repa (kam zapsat shopify_*.md)')
    parser.add_argument('--branch', default='w1-28', help='Větev pro GitHub odkazy (default w1-28)')
    args = parser.parse_args()

    src_root = Path(args.src)
    out_root = Path(args.out)
    objects = collect_objects(src_root, args.branch)

    by_type = {}
    for obj in objects:
        by_type.setdefault(obj['type'], []).append(obj)

    counts = ', '.join(f'{t}: {len(v)}' for t, v in sorted(by_type.items()))
    print(f'Načteno {len(objects)} objektů ({counts})')

    write_md(out_root / 'shopify_tables.md', 'Tabulky (Tables)', [
        ('Tabulky (Tables)', by_type.get('table', []), False),
        ('Rozšíření tabulek (Table Extensions)', by_type.get('tableextension', []), True),
    ])
    write_md(out_root / 'shopify_pages.md', 'Stránky (Pages)', [
        ('Stránky (Pages)', by_type.get('page', []), False),
        ('Rozšíření stránek (Page Extensions)', by_type.get('pageextension', []), True),
    ])
    write_md(out_root / 'shopify_codeunits.md', 'Codeunity (Codeunits)', [
        ('Codeunity (Codeunits)', by_type.get('codeunit', []), False),
    ])
    write_md(out_root / 'shopify_reports.md', 'Reporty (Reports)', [
        ('Reporty (Reports)', by_type.get('report', []), False),
        ('Rozšíření reportů (Report Extensions)', by_type.get('reportextension', []), True),
    ])


if __name__ == '__main__':
    main()
