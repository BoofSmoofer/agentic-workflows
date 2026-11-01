#!/usr/bin/env python3
"""Validate portable package paths, Markdown links and pinned reference bytes."""
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/engineering-workflow'


def anchors(text):
    result = set()
    counts = {}
    for line in text.splitlines():
        match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if match:
            value = re.sub(r'[^\w\- ]', '', match[1].lower()).replace(' ', '-')
            count = counts.get(value, 0)
            counts[value] = count + 1
            result.add(value + (f'-{count}' if count else ''))
    return result


def validate():
    errors = []
    skill = (SKILL / 'SKILL.md').read_text()
    if not skill.startswith('---\nname: engineering-workflow\ndescription: '):
        errors.append('Missing/invalid coordinator frontmatter')
    if '/Users/' in skill or '/Users/' in (SKILL / 'references/session-handoff.md').read_text():
        errors.append('Machine-specific path leaked into portable workflow')
    manifest = json.loads((SKILL / 'vendor/manifest.json').read_text())
    recorded = set()
    for source in manifest['sources']:
        for name, record in source['files'].items():
            path = SKILL / name
            recorded.add(path)
            if not path.is_file():
                errors.append(f'Missing upstream file: {name}')
                continue
            data = path.read_bytes()
            blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if hashlib.sha256(data).hexdigest() != record['sha256'] or blob != record['git_blob_sha']:
                errors.append(f'Upstream bytes changed: {name}')
    vendor_files = set(p for p in (SKILL / 'vendor').rglob('*') if p.is_file()) - {SKILL / 'vendor/manifest.json'}
    if vendor_files != recorded:
        errors.append('Vendor file set differs from pinned manifest')
    for path in ROOT.rglob('*.md'):
        content = path.read_text()
        # Markdown links only, including pinned upstream references; skip illustrative fenced code.
        visible = re.sub(r'```.*?```', '', content, flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', visible):
            target = target.strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            filepart, _, fragment = unquote(target).partition('#')
            dest = (path.parent / filepart).resolve() if filepart else path.resolve()
            if not dest.is_relative_to(ROOT.resolve()) or not dest.exists():
                errors.append(f'{path.relative_to(ROOT)}: broken local link {target}')
            elif fragment and dest.is_file() and fragment not in anchors(dest.read_text()):
                errors.append(f'{path.relative_to(ROOT)}: missing anchor {target}')
    for error in errors:
        print(error, file=sys.stderr)
    if not errors:
        print(f'PASS: coordinator, local links/anchors, portable paths and {len(recorded)} pinned upstream files')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(validate())
