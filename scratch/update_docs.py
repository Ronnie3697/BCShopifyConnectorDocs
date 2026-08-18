#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aktualizace dokumentace Shopify Connectoru z GitHubu.

Stáhne/aktualizuje sparse-checkout repa StefanMaron/MSDyn365BC.Code.History
(jen složka `Shopify/`), a pokud přibyly změny, přegeneruje markdown
dokumentaci přes parse_al.py. Na konci vypíše přehled commitů (minor verzí)
od posledního běhu — podklad pro ruční doplnění VersionChanges/*.md.

Použití:
    python update_docs.py                  # update aktuální větve (w1-28)
    python update_docs.py --check-latest   # zjistí nejnovější w1-* větev
    python update_docs.py --branch w1-29   # přepne na jinou větev
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_URL = 'https://github.com/StefanMaron/MSDyn365BC.Code.History.git'
SCRIPT_DIR = Path(__file__).resolve().parent
DOCS_ROOT = SCRIPT_DIR.parent
# Checkout záměrně MIMO OneDrive (žádný sync tisíců souborů) a s krátkou cestou
# (Windows MAX_PATH) — viz ⚠️ v README.
CHECKOUT = Path(os.environ.get('LOCALAPPDATA', SCRIPT_DIR)) / 'BCShopifyConnectorDocs' / 'msdyn'
DEFAULT_BRANCH = 'w1-28'


def run(args, cwd=None, capture=True):
    result = subprocess.run(args, cwd=cwd, capture_output=capture, text=True, encoding='utf-8')
    if result.returncode != 0:
        out = (result.stderr or result.stdout or '').strip() if capture else ''
        sys.exit(f'Příkaz selhal ({" ".join(args)}):\n{out}')
    return (result.stdout or '').strip()


def latest_w1_branch():
    out = run(['git', 'ls-remote', '--heads', REPO_URL, 'refs/heads/w1-*'])
    majors = [int(m.group(1)) for m in re.finditer(r'refs/heads/w1-(\d+)$', out, re.MULTILINE)]
    if not majors:
        sys.exit('Na remote nenalezeny žádné w1-* větve.')
    return f'w1-{max(majors)}'


def ensure_checkout(branch: str):
    if not (CHECKOUT / '.git').exists():
        print(f'Klonuji {REPO_URL} (větev {branch}, sparse, bez blobů)...')
        CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        run(['git', 'clone', '--filter=blob:none', '--no-checkout',
             '--branch', branch, '--single-branch', REPO_URL, str(CHECKOUT)])
        # Windows: bez longpaths se dlouhé cesty tiše nevytvoří (chybělo by ~20 objektů)
        run(['git', 'config', 'core.longpaths', 'true'], cwd=CHECKOUT)
        run(['git', 'sparse-checkout', 'init', '--cone'], cwd=CHECKOUT)
        run(['git', 'sparse-checkout', 'set', 'Shopify'], cwd=CHECKOUT)
        run(['git', 'checkout', branch], cwd=CHECKOUT)
        return None  # čerstvý klon — žádné "předchozí" HEAD

    run(['git', 'config', 'core.longpaths', 'true'], cwd=CHECKOUT)
    current = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=CHECKOUT)
    old_head = run(['git', 'rev-parse', 'HEAD'], cwd=CHECKOUT)
    if current != branch:
        print(f'Přepínám {current} -> {branch}...')
        run(['git', 'remote', 'set-branches', 'origin', branch], cwd=CHECKOUT)
        run(['git', 'fetch', 'origin', branch], cwd=CHECKOUT)
        run(['git', 'checkout', '-B', branch, f'origin/{branch}'], cwd=CHECKOUT)
        return None  # jiná větev — diff proti staré nedává smysl
    print(f'Stahuji aktualizace větve {branch}...')
    run(['git', 'pull', '--ff-only'], cwd=CHECKOUT)
    return old_head


def verify_checkout_complete():
    """Kontrola, že checkout zapsal všechny soubory (past na Windows MAX_PATH)."""
    missing = run(['git', 'status', '--short'], cwd=CHECKOUT)
    if missing:
        sys.exit('Checkout je nekompletní (git status není čistý) — zkontroluj '
                 f'core.longpaths a délku cesty:\n{missing[:2000]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--branch', default=None, help=f'w1-* větev (default {DEFAULT_BRANCH})')
    parser.add_argument('--check-latest', action='store_true',
                        help='jen zjistí nejnovější w1-* větev na remote a skončí')
    args = parser.parse_args()

    if args.check_latest:
        latest = latest_w1_branch()
        print(f'Nejnovější větev na remote: {latest}')
        print(f'Pro přepnutí spusť: python {Path(__file__).name} --branch {latest}')
        return

    branch = args.branch or DEFAULT_BRANCH
    old_head = ensure_checkout(branch)
    verify_checkout_complete()
    new_head = run(['git', 'rev-parse', 'HEAD'], cwd=CHECKOUT)
    version = run(['git', 'log', '-1', '--format=%s'], cwd=CHECKOUT)
    print(f'Checkout na {version} ({new_head[:8]})')

    if old_head == new_head:
        print('Žádné nové commity — dokumentace je aktuální, ale pro jistotu přegeneruji.')
    else:
        if old_head:
            print('\nNové verze od posledního běhu (podklad pro VersionChanges):')
            log = run(['git', 'log', '--format=%h %ad %s', '--date=short',
                       f'{old_head}..{new_head}'], cwd=CHECKOUT)
            print(log or '(žádné)')
            print('\nDiff staty per verze zobrazíš např.:')
            print(f'  git -C "{CHECKOUT}" diff --stat <sha1>..<sha2> -- "Shopify/app"')

    sys.stdout.flush()
    run([sys.executable, str(SCRIPT_DIR / 'parse_al.py'),
         '--src', str(CHECKOUT), '--out', str(DOCS_ROOT), '--branch', branch],
        capture=False)
    print('\nHotovo. Nezapomeň zkontrolovat git diff dokumentace a doplnit VersionChanges.')


if __name__ == '__main__':
    main()
