#!/usr/bin/env python3
"""Build a reproducible per-file and symbol catalog for the Paperclip fork."""
from __future__ import annotations
import json, re, subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "engineering" / "catalog"
OUT.mkdir(parents=True, exist_ok=True)

TEXT_EXT = {'.ts','.tsx','.js','.jsx','.mjs','.cjs','.py','.sh','.bash','.md','.mdx','.json','.yaml','.yml','.toml','.sql','.css','.scss','.html','.xml','.txt','.env'}
SOURCE_EXT = {'.ts','.tsx','.js','.jsx','.mjs','.cjs','.py','.sh','.bash','.sql'}

def tracked_files():
    data = subprocess.check_output(['git','ls-files','-z'], cwd=ROOT)
    return [Path(x) for x in data.decode().split('\0') if x]

def layer(path: str) -> str:
    p = Path(path)
    parts = p.parts
    if path.startswith('server/'): return 'server'
    if path.startswith('ui/'): return 'ui'
    if path.startswith('cli/'): return 'cli'
    if path.startswith('packages/db/'): return 'database'
    if path.startswith('packages/shared/'): return 'shared-contracts'
    if path.startswith('packages/adapters/'): return 'adapters'
    if path.startswith('packages/plugins/'): return 'plugins'
    if path.startswith('packages/paperclip-runner/'): return 'runner'
    if path.startswith('packages/'): return 'packages'
    if path.startswith('tests/'): return 'tests'
    if path.startswith('doc/') or path.startswith('docs/'): return 'documentation'
    if path.startswith('engineering/'): return 'engineering-meta'
    if path.startswith('skills/'): return 'runtime-skills'
    if path.startswith('scripts/'): return 'build-ops'
    if path.startswith('docker/'): return 'deployment'
    if p.name.startswith('.') or p.name in {'AGENTS.md','README.md'}: return 'repository-meta'
    return 'root'

def role(path: str, ext: str) -> str:
    p = path.lower()
    if path.startswith(('doc/','docs/')) or ext in {'.md','.mdx'}: return 'documentation'
    if path.startswith('tests/') or '/__tests__/' in path: return 'test-fixture'
    if path.startswith('engineering/'): return 'engineering-index'
    if 'migration' in p or ext == '.sql': return 'schema-migration'
    if path.startswith(('scripts/','docker/')) or ext in {'.sh','.bash'}: return 'build/deployment-script'
    if ext in {'.json','.yaml','.yml','.toml'}: return 'configuration/data'
    if ext in SOURCE_EXT: return 'source-code'
    return 'asset/other'

def classify_domain(path: str) -> list[str]:
    p = path.lower()
    vals=[]
    for key, label in [('auth','authentication'),('heartbeat','heartbeat-execution'),('runner','runner'),('adapter','adapter'),('plugin','plugin'),('skill','skills'),('connector','connectors'),('workspace','workspace'),('mcp','mcp'),('database','database'),('migration','database'),('cost','budgets-costs'),('budget','budgets-costs'),('approval','governance'),('recovery','recovery'),('sandbox','sandbox'),('telemetry','telemetry'),('observability','observability'),('slack','chat-connectors'),('github','github-integration'),('hermes','hermes-integration'),('story','ui-storybook'),('e2e','testing'),('release','release')]:
        if key in p and label not in vals: vals.append(label)
    return vals or ['general']

def symbols(text: str, ext: str) -> list[dict]:
    if ext not in SOURCE_EXT: return []
    pats = [
      ('function', r'\b(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)'),
      ('class', r'\b(?:export\s+default\s+|export\s+)?class\s+([A-Za-z_$][\w$]*)'),
      ('interface', r'\b(?:export\s+)?interface\s+([A-Za-z_$][\w$]*)'),
      ('type', r'\b(?:export\s+)?type\s+([A-Za-z_$][\w$]*)\s*[=<]'),
      ('const', r'\b(?:export\s+)?const\s+([A-Za-z_$][\w$]*)\s*='),
      ('python-def', r'^\s*(?:async\s+)?def\s+([A-Za-z_]\w*)\s*\(',),
      ('shell-function', r'^\s*([A-Za-z_]\w*)\s*\(\)\s*\{'),
    ]
    out=[]; seen=set()
    lines=text.splitlines()
    for kind, pat in pats:
        for m in re.finditer(pat, text, re.M):
            name=m.group(1)
            key=(kind,name)
            if key in seen: continue
            seen.add(key)
            line=text.count('\n',0,m.start())+1
            out.append({'kind':kind,'name':name,'line':line})
    return sorted(out, key=lambda x:x['line'])[:300]

def imports(text: str, ext: str) -> list[str]:
    if ext not in {'.ts','.tsx','.js','.jsx','.mjs','.cjs'}: return []
    vals=set()
    for pat in [r'\bfrom\s+[\'\"]([^\'\"]+)', r'\bimport\s*[\(]?\s*[\'\"]([^\'\"]+)', r'\brequire\(\s*[\'\"]([^\'\"]+)']:
        vals.update(re.findall(pat,text))
    return sorted(vals)[:200]

def headings(text: str) -> list[str]:
    return [re.sub(r'^#+\s*','',x).strip() for x in text.splitlines() if re.match(r'^#{1,6}\s+',x)][:100]

def env_vars(text: str) -> list[str]:
    return sorted(set(re.findall(r'\b(?:PAPERCLIP|DATABASE|BETTER_AUTH|OPENAI|ANTHROPIC|GITHUB|AWS|SENTRY|OTEL|MCP)_[A-Z0-9_]+\b', text)))[:200]

files=[]; counts=Counter(); symbol_rows=[]; domain_files=defaultdict(list)
for rel in tracked_files():
    path=rel.as_posix(); ext=rel.suffix.lower(); counts['tracked']+=1
    try: raw=(ROOT/rel).read_bytes()
    except OSError: continue
    binary=b'\x00' in raw[:8192]
    text='' if binary or ext not in TEXT_EXT else raw.decode('utf-8','replace')
    item={'path':path,'layer':layer(path),'role':role(path,ext),'domain':classify_domain(path),'extension':ext or '(none)','bytes':len(raw),'lines':None if binary else text.count('\n')+ (1 if text else 0),'binary':binary,'confidence':'automated-structural'}
    if text:
        item.update({'headings':headings(text),'symbols':symbols(text,ext),'imports':imports(text,ext),'environment_variables':env_vars(text)})
        if ext in SOURCE_EXT:
            for s in item['symbols']:
                symbol_rows.append({'path':path,**s,'layer':item['layer'],'domain':item['domain']})
    files.append(item); counts[item['role']]+=1
    for d in item['domain']: domain_files[d].append(path)

commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
meta={'schema_version':'1.0','generated_at':datetime.now(timezone.utc).isoformat(),'commit':commit,'method':'git-tracked-file structural scan; regex symbol extraction; source docs remain authoritative','limitations':['No AST or runtime call graph was produced.','Generated metadata describes file structure and naming signals, not proof that every path executes.','Semantic ownership must be confirmed by source tests and live runtime traces.'],'counts':dict(counts),'files':files,'symbols':symbol_rows,'domains':{k:sorted(v) for k,v in sorted(domain_files.items())}}
(OUT/'FILE_CATALOG.json').write_text(json.dumps(meta,indent=2,sort_keys=False)+'\n')

lines=['# Code and File Catalog','',f'Generated: `{meta["generated_at"]}`',f'Indexed commit: `{commit}`','', 'This catalog is generated from `git ls-files`. It provides structural metadata for every tracked file and extracted symbols for source files. It is an index, not a replacement for code review or runtime proof.', '', '## Inventory counts','']
for k,v in sorted(counts.items()): lines.append(f'- `{k}`: {v}')
lines += ['', '## Architectural layers', '']
for k,v in sorted(domain_files.items()): lines.append(f'- **{k}** — {len(v)} files')
lines += ['', '## How to regenerate','', '```sh','python3 engineering/scripts/build_code_catalog.py','```','', 'Machine-readable detail is in `engineering/catalog/FILE_CATALOG.json`. The catalog deliberately uses `confidence: automated-structural`; update `engineering/ARCHITECTURE.md` or a decision record when semantic interpretation is confirmed.']
(OUT/'README.md').write_text('\n'.join(lines)+'\n')

sym=['# Function and Symbol Index','',f'Generated from commit `{commit}`.', '', '| Kind | Symbol | File | Line | Domain |','|---|---|---|---:|---|']
for row in sorted(symbol_rows,key=lambda x:(x['path'],x['line'],x['name'])):
    sym.append(f"| `{row['kind']}` | `{row['name']}` | `{row['path']}` | {row['line']} | {', '.join(row['domain'])} |")
(OUT/'FUNCTION_INDEX.md').write_text('\n'.join(sym)+'\n')
print(f'indexed {len(files)} files and {len(symbol_rows)} symbols; output {OUT}')
