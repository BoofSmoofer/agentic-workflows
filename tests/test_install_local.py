import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/install-local.py'
spec = importlib.util.spec_from_file_location('installer', SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class LocalInstallation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Installer test')
        (self.root / 'team.txt').write_text('existing team content\n')
        self.git('add', 'team.txt')
        self.git('commit', '-qm', 'baseline')
        self.exclude = self.root / '.git/info/exclude'
        self.exclude.write_bytes(b'# existing local rule\nprivate-local-file')
        self.before_exclude = self.exclude.read_bytes()
        self.before_index = (self.root / '.git/index').read_bytes()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True)

    def install(self, client='codex', dry_run=False, project=None):
        with contextlib.redirect_stdout(io.StringIO()):
            installer.install(project or self.root, client, dry_run)

    def test_install_both_clients_preserves_index_and_existing_work(self):
        (self.root / 'team.txt').write_text('uncommitted change\n')
        self.install()
        self.install('claude')
        for directory in ('.agents', '.claude'):
            self.assertTrue((self.root / directory / 'skills/engineering-workflow/SKILL.md').is_file())
            self.assertTrue((self.root / directory / 'skills/engineering-workflow/vendor/testdouble-han/LICENSE').is_file())
        self.assertTrue(self.exclude.read_bytes().startswith(self.before_exclude))
        self.assertEqual(self.before_index, (self.root / '.git/index').read_bytes())
        self.assertEqual(self.git('status', '--porcelain'), ' M team.txt\n')
        self.assertEqual(self.git('ls-files', '--', '.agents', '.claude', '.agent-work'), '')

    def test_dry_run_writes_nothing(self):
        self.install(dry_run=True)
        self.assertEqual(self.before_exclude, self.exclude.read_bytes())
        self.assertFalse((self.root / '.agents').exists())

    def test_refuse_existing_installation(self):
        self.install()
        path = self.root / '.agents/skills/engineering-workflow/SKILL.md'
        path.write_text('personal changes')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.install()
        self.assertEqual(path.read_text(), 'personal changes')

    def test_refuse_tracked_artifacts(self):
        artifacts = self.root / '.agent-work'
        artifacts.mkdir()
        (artifacts / 'team.md').write_text('tracked')
        self.git('add', '.agent-work/team.md')
        with self.assertRaisesRegex(ValueError, 'tracked personal path'):
            self.install()
        self.assertFalse((self.root / '.agents').exists())

    def test_refuse_tracked_skill_even_when_working_file_deleted(self):
        path = self.root / '.agents/skills/engineering-workflow/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('tracked')
        self.git('add', str(path.relative_to(self.root)))
        self.git('commit', '-qm', 'tracked skill')
        path.unlink()
        path.parent.rmdir()
        with self.assertRaisesRegex(ValueError, 'tracked personal path'):
            self.install()

    def test_refuse_symlinked_parent(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (self.root / '.agents').symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlinked'):
            self.install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_refuse_project_ignore_override_before_copy(self):
        (self.root / '.gitignore').write_text('!.agents/skills/engineering-workflow/\n!.agents/skills/engineering-workflow/**\n')
        with self.assertRaisesRegex(ValueError, 'Expected protection|not effective'):
            self.install()
        self.assertFalse((self.root / '.agents').exists())

    def test_project_subdirectory_is_rejected(self):
        nested = self.root / 'nested'
        nested.mkdir()
        with self.assertRaisesRegex(ValueError, 'checkout root'):
            self.install(project=nested)

    def test_linked_worktree(self):
        worktree = Path(self.temp.name) / 'linked'
        self.git('worktree', 'add', '-qb', 'test-linked', str(worktree))
        self.install(project=worktree)
        self.assertTrue((worktree / '.agents/skills/engineering-workflow/SKILL.md').is_file())
        self.assertFalse((self.root / '.agents').exists())
        self.assertEqual(subprocess.check_output(['git', '-C', str(worktree), 'status', '--porcelain'], text=True), '')


if __name__ == '__main__':
    unittest.main()
