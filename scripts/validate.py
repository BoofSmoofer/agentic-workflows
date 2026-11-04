#!/usr/bin/env python3
"""Validate portable package paths, Markdown links and pinned reference bytes."""
from pathlib import Path
import hashlib
import json
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ('engineering-workflow', 'local-pr-workflow')


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
    pinned_count = 0
    for skill_name in SKILLS:
        directory = ROOT / 'skills' / skill_name
        skill = (directory / 'SKILL.md').read_text()
        if not skill.startswith(f'---\nname: {skill_name}\ndescription: '):
            errors.append(f'{skill_name}: missing/invalid coordinator frontmatter')
        for path in directory.rglob('*.md'):
            if '/Users/' in path.read_text():
                errors.append(f'{path.relative_to(ROOT)}: machine-specific path in portable workflow')
        manifest = json.loads((directory / 'vendor/manifest.json').read_text())
        recorded = set()
        for source in manifest['sources']:
            for name, record in source['files'].items():
                path = directory / name
                recorded.add(path)
                if not path.is_file():
                    errors.append(f'{skill_name}: missing upstream file: {name}')
                    continue
                data = path.read_bytes()
                blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                if hashlib.sha256(data).hexdigest() != record['sha256'] or blob != record['git_blob_sha']:
                    errors.append(f'{skill_name}: upstream bytes changed: {name}')
        vendor_files = set(p for p in (directory / 'vendor').rglob('*') if p.is_file()) - {directory / 'vendor/manifest.json'}
        if vendor_files != recorded:
            errors.append(f'{skill_name}: vendor file set differs from pinned manifest')
        pinned_count += len(recorded)
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
        print(f'PASS: {len(SKILLS)} coordinators, local links/anchors, portable paths and {pinned_count} pinned upstream files')
    return bool(errors)


if __name__ == '__main__':
    sys.exit(validate())
