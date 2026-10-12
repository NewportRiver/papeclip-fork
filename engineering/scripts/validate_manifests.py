#!/usr/bin/env python3
"""Validate Paperclip domain manifest structure without requiring dependencies."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
MAN=ROOT/'engineering/manifests'
required=('Evidence:','## Verification','## Gaps')
errors=[]
for p in sorted(MAN.glob('*.md')):
    if p.name in {'MANIFEST_SCHEMA.md','CONTRACT_ID_RULES.md','CONFIGURATION_INDEX.md','SECURITY_SIDE_EFFECT_MATRIX.md'}:
        continue
    text=p.read_text()
    if not text.startswith('# '): errors.append(f'{p}: missing title')
    for token in required:
        if token not in text: errors.append(f'{p}: missing {token}')
    if '## Owning areas' not in text and '## Responsibilities' not in text: errors.append(f'{p}: missing ownership/responsibility section')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'VALID: {len(list(MAN.glob("*.md")))-4} domain manifests')
