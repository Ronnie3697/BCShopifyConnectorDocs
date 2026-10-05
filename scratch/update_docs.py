#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aktualizace dokumentace Shopify Connectoru z GitHubu.

Stáhne/aktualizuje sparse-checkout repa microsoft/BCApps
(jen složka `src/Apps/W1/Shopify/`) a přegeneruje markdown
dokumentaci přes parse_al.py. Na konci vypíše přehled commitů (minor verzí)
od posledního běhu — podklad pro ruční doplnění VersionChanges/*.md.

Použití:
    python update_docs.py                  # update releases/28.5
    python update_docs.py --check-latest   # zjistí nejnovější číselnou release větev
    python update_docs.py --branch releases/28.6  # přepne na jinou větev
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_URL = 'https://github.com/microsoft/BCApps.git'
SCRIPT_DIR = Path(__file__).resolve().parent
DOCS_ROOT = SCRIPT_DIR.parent
# Checkout záměrně MIMO OneDrive (žádný sync tisíců souborů) a s krátkou cestou
# (Windows MAX_PATH) — viz ⚠️ v README.
CHECKOUT = Path(os.environ.get('LOCALAPPDATA', SCRIPT_DIR)) / 'BCShopifyConnectorDocs' / 'bcapps'
DEFAULT_BRANCH = 'releases/28.5'
SHOPIFY_ROOT = 'src/Apps/W1/Shopify'


def run(args, cwd=None, capture=True):
    result = subprocess.run(args, cwd=cwd, capture_output=capture, text=True, encoding='utf-8')
    if result.returncode != 0:
        out = (result.stderr or result.stdout or '').strip() if capture else ''
        sys.exit(f'Příkaz selhal ({" ".join(args)}):\n{out}')
    return (result.stdout or '').strip()


def latest_release_branch():
    out = run(['git', 'ls-remote', '--heads', REPO_URL, 'refs/heads/releases/*'])
    versions = [tuple(map(int, m.groups())) for m in
                re.finditer(r'refs/heads/releases/(\d+)\.(\d+)$', out, re.MULTILINE)]
    if not versions:
        sys.exit('Na remote nenalezeny žádné číselné release větve.')
    major, minor = max(versions)
    return f'releases/{major}.{minor}'


def ensure_checkout(branch: str):
    if not (CHECKOUT / '.git').exists():
        print(f'Klonuji {REPO_URL} (větev {branch}, sparse, bez blobů)...')
        CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        run(['git', 'clone', '--filter=blob:none', '--no-checkout',
             '--branch', branch, '--single-branch', REPO_URL, str(CHECKOUT)])
        # Windows: bez longpaths se dlouhé cesty tiše nevytvoří (chybělo by ~20 objektů)
        run(['git', 'config', 'core.longpaths', 'true'], cwd=CHECKOUT)
        run(['git', 'sparse-checkout', 'init', '--cone'], cwd=CHECKOUT)
        run(['git', 'sparse-checkout', 'set', SHOPIFY_ROOT], cwd=CHECKOUT)
        run(['git', 'checkout', branch], cwd=CHECKOUT)
        return None  # čerstvý klon — žádné "předchozí" HEAD

    verify_checkout_complete()
    run(['git', 'config', 'core.longpaths', 'true'], cwd=CHECKOUT)
    current = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=CHECKOUT)
    old_head = run(['git', 'rev-parse', 'HEAD'], cwd=CHECKOUT)
    if current != branch:
        print(f'Přepínám {current} -> {branch}...')
        run(['git', 'remote', 'set-branches', 'origin', branch], cwd=CHECKOUT)
        run(['git', 'fetch', 'origin', branch], cwd=CHECKOUT)
        run(['git', 'checkout', branch], cwd=CHECKOUT)
        run(['git', 'merge', '--ff-only', f'origin/{branch}'], cwd=CHECKOUT)
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
    parser.add_argument('--branch', default=None, help=f'release větev (default {DEFAULT_BRANCH})')
    parser.add_argument('--check-latest', action='store_true',
                        help='jen zjistí nejnovější číselnou release větev na remote a skončí')
    args = parser.parse_args()

    if args.check_latest:
        latest = latest_release_branch()
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
                       f'{old_head}..{new_head}', '--', SHOPIFY_ROOT], cwd=CHECKOUT)
            print(log or '(žádné)')
            print('\nDiff staty per verze zobrazíš např.:')
            print(f'  git -C "{CHECKOUT}" diff --stat <sha1>..<sha2> -- "{SHOPIFY_ROOT}/App"')

    sys.stdout.flush()
    run([sys.executable, str(SCRIPT_DIR / 'parse_al.py'),
         '--src', str(CHECKOUT), '--out', str(DOCS_ROOT), '--branch', branch],
        capture=False)
    print('\nHotovo. Nezapomeň zkontrolovat git diff dokumentace a doplnit VersionChanges.')


if __name__ == '__main__':
    main()
