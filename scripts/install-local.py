#!/usr/bin/env python3
"""Copy the self-contained skill into one explicitly selected project checkout."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def git(project, *args, check=True):
    return subprocess.run(['git', '-C', str(project), *args], check=check,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def install(project, client, dry_run=False):
    project = Path(project).expanduser().resolve(strict=True)
    actual = Path(git(project, 'rev-parse', '--show-toplevel').stdout.strip()).resolve()
    if actual != project:
        raise ValueError('--project must be the Git checkout root')
    source = Path(__file__).resolve().parents[1] / 'skills/engineering-workflow'
    if not (source / 'SKILL.md').is_file():
        raise ValueError('Source skill is missing; run from a complete library checkout')
    if project == Path(__file__).resolve().parents[1]:
        raise ValueError('Choose another project, not the workflow source library')
    relative = Path('.agents' if client == 'codex' else '.claude') / 'skills/engineering-workflow'
    destination = project / relative
    for path in (relative, Path('.agent-work')):
        cursor = project
        for part in path.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError(f'Refusing symlinked personal path: {cursor}')
            if cursor.exists() and not cursor.is_dir():
                raise ValueError(f'Expected a directory: {cursor}')
    if destination.exists():
        raise ValueError(f'Installation already exists; review/back it up before replacing: {destination}')
    # Include a slash so a file with the same prefix cannot evade Git path checks.
    for path in (relative, Path('.agent-work')):
        if git(project, 'ls-files', '-z', '--', str(path)).stdout:
            raise ValueError(f'Refusing tracked personal path: {path}')
    exclude = Path(git(project, 'rev-parse', '--git-path', 'info/exclude').stdout.strip())
    if not exclude.is_absolute():
        exclude = project / exclude
    if exclude.is_symlink() or exclude.parent.is_symlink():
        raise ValueError('Refusing symlinked local exclude file/directory')
    old = exclude.read_bytes() if exclude.exists() else b''
    rules = ['/' + relative.as_posix() + '/', '/.agent-work/']
    existing = old.decode('utf-8').splitlines()
    additions = [r for r in rules if r not in existing]
    print(f'Project: {project}\nClient: {client}\nDestination: {destination}\nLocal excludes: {exclude}')
    if dry_run:
        print('Dry run: would add missing local rules and copy the complete skill; no files changed.')
        return
    if additions:
        exclude.parent.mkdir(parents=True, exist_ok=True)
        with exclude.open('ab') as handle:
            if old and not old.endswith(b'\n'):
                handle.write(b'\n')
            handle.write(('\n# Personal engineering workflow\n' + '\n'.join(additions) + '\n').encode())
    # Check the rule source before copying: project .gitignore rules take precedence.
    probes = [str(relative / p.relative_to(source)) for p in source.rglob('*') if p.is_file()]
    probes.append('.agent-work/example/state.md')
    for probe in probes:
        result = git(project, 'check-ignore', '-v', '--no-index', '--', probe, check=False)
        if result.returncode != 0 or '\t' not in result.stdout:
            raise ValueError(f'Local exclusion not effective: {probe}; nothing copied')
        provenance, _ = result.stdout.rstrip('\n').split('\t', 1)
        source_path, _, pattern = provenance.rsplit(':', 2)
        resolved = Path(source_path)
        if not resolved.is_absolute():
            resolved = project / resolved
        if resolved.resolve() != exclude.resolve() or pattern.startswith('!'):
            raise ValueError(f'Expected protection from local info/exclude for {probe}; nothing copied')
    # Never follow source links; a source update must remain a real self-contained tree.
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Source contains symlinks; refusing installation')
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)
    print('Installed. Personal paths are locally ignored; no index or global settings changed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, help='Root of another Git checkout')
    parser.add_argument('--client', required=True, choices=('codex', 'claude'))
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        install(args.project, args.client, args.dry_run)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f'Install stopped: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
