#!/usr/bin/env python3
"""Check whether generated Paperclip catalogs match the current Git tree."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CAT=ROOT/'engineering/catalog/FILE_CATALOG.json'
MARK=ROOT/'engineering/markers/MARKER_INDEX.json'

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    errors=[]
    head=git('rev-parse','HEAD')
    tracked=git('ls-files').splitlines()
    data=json.loads(CAT.read_text())
    indexed={x['path'] for x in data['files']}
    expected=set(tracked)
    if data.get('commit') != head:
        errors.append(f'catalog source commit {data.get("commit")} != HEAD {head}')
    if indexed != expected:
        errors.append(f'catalog paths differ: indexed={len(indexed)} tracked={len(expected)} missing={len(expected-indexed)} extra={len(indexed-expected)}')
    if MARK.exists():
        marker=json.loads(MARK.read_text())
        if marker.get('source_catalog_commit') != data.get('commit'):
            errors.append('marker index source commit does not match catalog')
    if errors:
        print('STALE')
        for e in errors: print(f'- {e}')
        return 1
    print(f'FRESH: {len(expected)} tracked files, catalog commit {head}')
    return 0

if __name__ == '__main__': sys.exit(main())
