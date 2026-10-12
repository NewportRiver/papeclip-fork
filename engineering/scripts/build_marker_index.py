#!/usr/bin/env python3
"""Generate stable coded markers and task cross-references for the AU plan."""
from __future__ import annotations
import hashlib, json, re, subprocess
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CATALOG=ROOT/'engineering/catalog/FILE_CATALOG.json'
TASKS=ROOT/'engineering/plan/TASKS.md'
OUT=ROOT/'engineering/markers'; OUT.mkdir(parents=True,exist_ok=True)

def code(prefix, value):
    digest=hashlib.sha1(value.encode()).hexdigest()[:10].upper()
    return f'{prefix}-{digest}'

data=json.loads(CATALOG.read_text())
task_text=TASKS.read_text()
tasks=re.findall(r'^### (AU-\d+) — (.+)$',task_text,re.M)

def marker_file(item):
    return {'id':code('F',item['path']),'kind':'file','path':item['path'],'layer':item['layer'],'role':item['role'],'domain':item['domain'],'evidence':'structural'}

def marker_symbol(item):
    key=f"{item['path']}::{item['kind']}::{item['name']}::{item['line']}"
    return {'id':code('S',key),'kind':'symbol','path':item['path'],'name':item['name'],'symbol_kind':item['kind'],'line':item['line'],'layer':item['layer'],'domain':item['domain'],'evidence':'structural'}

files=[marker_file(x) for x in data['files']]
symbols=[marker_symbol(x) for x in data['symbols']]
file_by_path={x['path']:x for x in files}
syms_by_path={}
for x in symbols: syms_by_path.setdefault(x['path'],[]).append(x)

# Task-to-domain retrieval rules. These are intentionally explicit and reviewable.
rules={
'AU-001':['engineering/','AGENTS.md','README.md'],
'AU-002':['engineering/ENGINEERING_FUNDAMENTALS.md','engineering/AGENTIC-UNDERSTANDING-ROADMAP.md'],
'AU-003':['engineering/catalog/','engineering/scripts/'],
'AU-010':['engineering/plan/','engineering/catalog/'],
'AU-011':['server/src/routes/','server/src/services/','server/src/auth/','packages/shared/src/','server/package.json','doc/DEPLOYMENT-MODES.md'],
'AU-012':['packages/db/','doc/DATABASE.md','scripts/backup-db.sh'],
'AU-013':['server/src/services/issues','server/src/services/companies','server/src/services/goals','server/src/services/projects','packages/db/src/schema/','doc/PRODUCT.md'],
'AU-014':['server/src/services/heartbeat','server/src/services/execution','server/src/services/recovery','packages/paperclip-runner/','doc/execution-semantics.md'],
'AU-015':['packages/adapters/','packages/plugins/','packages/hermes','server/src/services/adapters','README.md'],
'AU-016':['ui/src/','cli/','docker/','scripts/install.sh','doc/DOCKER.md','doc/DEPLOYMENT-MODES.md'],
'AU-017':['server/src/services/connectors/','server/src/services/mcp','packages/skills-catalog/','server/src/services/workspaces','packages/plugins/sandbox-providers/'],
'AU-018':['tests/','server/src/__tests__/','ui/','packages/'],
'AU-019':['engineering/catalog/','engineering/scripts/','package.json'],
'AU-020':['engineering/markers/','engineering/catalog/'],
'AU-021':['server/src/routes/','server/src/services/','packages/db/src/schema/','packages/shared/src/'],
'AU-022':['server/src/services/heartbeat','server/src/services/execution','packages/paperclip-runner/','tests/runner-recovery/'],
'AU-023':['.env.example','server/src/','packages/','doc/DATABASE.md','doc/DOCKER.md'],
'AU-024':['server/src/auth/','server/src/services/connectors/','server/src/services/mcp','packages/plugins/','doc/SECURITY.md'],
'AU-030':['package.json','scripts/','doc/DEVELOPING.md','doc/DOCKER.md'],
'AU-031':['scripts/','server/src/index','doc/DEVELOPING.md','doc/DATABASE.md'],
'AU-032':['server/src/auth/','cli/','doc/DEPLOYMENT-MODES.md'],
'AU-033':['server/src/services/','ui/src/','skills/paperclip/','doc/PRODUCT.md'],
'AU-034':['packages/db/','scripts/backup-db.sh','doc/DATABASE.md'],
'AU-035':['server/src/services/heartbeat','packages/adapters/','tests/'],
'AU-036':['server/src/services/recovery','server/src/services/heartbeat','packages/paperclip-runner/','tests/runner-recovery/'],
'AU-037':['packages/adapters/hermes','docker/hermes','scripts/smoke/hermes','README.md'],
'AU-038':['server/src/services/connectors/','server/src/services/mcp','packages/plugins/','tests/'],
'AU-040':['engineering/catalog/','engineering/markers/','engineering/plan/'],
'AU-041':['skills/paperclip/','engineering/','scripts/'],
'AU-042':['packages/db/','scripts/backup-db.sh','engineering/'],
'AU-043':['packages/adapters/','packages/hermes','tests/runner-recovery/'],
'AU-044':['.github/','doc/SECURITY.md','scripts/','engineering/'],
'AU-050':['engineering/catalog/','engineering/scripts/','engineering/plan/'],
'AU-051':['engineering/','scripts/','git'],
'AU-052':['engineering/','AGENTS.md','README.md'],
'AU-053':['engineering/','scripts/'],
'AU-054':['engineering/catalog/','engineering/plan/','tests/'],
}

def matches(path, needles):
    return any(n in path for n in needles)

# Keep task maps useful: cap broad rules and rank exact prefixes first.
task_map={}
for tid,title in tasks:
    needles=rules.get(tid,[])
    candidates=[x for x in files if matches(x['path'],needles)]
    candidates.sort(key=lambda x:(-max((len(n) for n in needles if n in x['path']),default=0),x['path']))
    # Prefer a reviewable bounded set; full catalog remains queryable by marker.
    selected=candidates[:80]
    fpaths={x['path'] for x in selected}
    ss=[s for s in symbols if s['path'] in fpaths]
    # prioritize named operational symbols and cap output
    ss.sort(key=lambda s:(0 if re.search(r'(run|task|heartbeat|auth|migrat|health|create|update|delete|stop|pause|recover|adapter|connect)',s['name'],re.I) else 1,s['path'],s['line']))
    task_map[tid]={'title':title,'file_markers':[x['id'] for x in selected],'symbol_markers':[x['id'] for x in ss[:120]],'retrieval_patterns':needles,'selection_note':'bounded path-pattern selection; query full catalog for additional markers'}

all_markers=files+symbols
assert len({x['id'] for x in all_markers})==len(all_markers)
registry={'schema_version':'1.0','source_catalog_commit':data['commit'],'marker_method':'SHA-1 prefix over stable path/symbol identity','marker_prefixes':{'F':'tracked file','S':'source symbol','D':'domain/contract (reserved)','T':'task (reserved)','C':'configuration/contract (reserved)','E':'evidence (reserved)'},'counts':{'files':len(files),'symbols':len(symbols),'tasks':len(task_map)},'markers':all_markers,'tasks':task_map}
(OUT/'MARKER_INDEX.json').write_text(json.dumps(registry,separators=(',',':'))+'\n')

summary=['# Marker Index','',f"Catalog source commit: `{data['commit']}`",'', 'Marker IDs are stable hashes of repository-relative identity. They are retrieval keys, not replacements for source paths.', '', '## Marker types', '', '- `F-XXXXXXXXXX` — tracked file.', '- `S-XXXXXXXXXX` — source symbol and line.', '- `D-XXXXXXXXXX` — reserved domain/contract marker.', '- `T-XXXXXXXXXX` — reserved task marker.', '- `C-XXXXXXXXXX` — reserved configuration/contract marker.', '- `E-XXXXXXXXXX` — reserved runtime evidence marker.', '', '## Counts', '', f'- Files: {len(files)}', f'- Symbols: {len(symbols)}', f'- AU tasks mapped: {len(task_map)}', '', '## Query examples', '', '```sh', "python3 - <<'PY'", "import json", "d=json.load(open('engineering/markers/MARKER_INDEX.json'))", "print(next(x for x in d['markers'] if x['path']=='server/src/index.ts'))", "print(d['tasks']['AU-035'])", "PY", '```', '', 'Full marker records and task cross-references are in `MARKER_INDEX.json`.']
(OUT/'README.md').write_text('\n'.join(summary)+'\n')

xref=['# Task-to-Marker Cross-Reference','', 'Generated from the code catalog and `engineering/plan/TASKS.md`.', '', 'Use task IDs to retrieve the relevant files first, then follow symbol markers and source/test links.']
for tid,title in tasks:
    m=task_map[tid]
    xref += ['',f'## {tid} — {title}','',f"Retrieval patterns: {', '.join('`'+x+'`' for x in m['retrieval_patterns'])}",'', 'File markers:']
    for mid in m['file_markers'][:30]:
        x=file_by_path[next(x['path'] for x in files if x['id']==mid)]
        xref.append(f"- `{mid}` `{x['path']}` — {x['role']} — {', '.join(x['domain'])}")
    if len(m['file_markers'])>30: xref.append(f"- … {len(m['file_markers'])-30} additional file markers in JSON")
    xref += ['', 'Priority symbol markers:']
    for sid in m['symbol_markers'][:25]:
        s=next(x for x in symbols if x['id']==sid)
        xref.append(f"- `{sid}` `{s['name']}` — `{s['path']}:{s['line']}`")
    if len(m['symbol_markers'])>25: xref.append(f"- … {len(m['symbol_markers'])-25} additional symbol markers in JSON")
(OUT/'TASK_MARKER_MAP.md').write_text('\n'.join(xref)+'\n')

# Task markers are explicit and stable from task IDs.
tasks_md=['# Task Markers','', 'These markers bind the development plan to the generated file/symbol registry.']
for tid,title in tasks:
    tasks_md.append(f'- `T-{tid}` — {title} — see `TASK_MARKER_MAP.md` and JSON key `{tid}`')
(OUT/'TASK_MARKERS.md').write_text('\n'.join(tasks_md)+'\n')
print(f'generated {len(files)} file markers, {len(symbols)} symbol markers, {len(task_map)} task maps')
