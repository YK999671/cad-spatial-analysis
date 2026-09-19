"""Read-only drawing inventory. Emits JSON; never opens CAD software or writes files."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from datetime import datetime, timezone

KINDS = {'.dwg': 'cad', '.dxf': 'cad', '.pdf': 'pdf',
         '.png': 'image', '.jpg': 'image', '.jpeg': 'image',
         '.tif': 'image', '.tiff': 'image', '.bmp': 'image', '.webp': 'image'}


def linked(path):
    data = path.lstat()
    return path.is_symlink() or bool(getattr(data, 'st_file_attributes', 0)
                                    & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0x400))


def inventory(source):
    root = Path(os.path.abspath(os.path.expanduser(source)))
    result = {'input': str(root), 'generated_at': datetime.now(timezone.utc).isoformat(),
              'files': [], 'skipped_links': [], 'errors': [],
              'scope': 'file inventory only; no drawing identity or connectivity inferred'}
    if not root.exists():
        result['errors'].append({'path': str(root), 'error': 'Input does not exist'})
        return result

    def add_file(path):
        suffix = path.suffix.lower()
        if suffix not in KINDS:
            return
        try:
            before = path.stat()
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
            after = path.stat()
            result['files'].append({
                'path': str(path), 'relative_path': str(path.relative_to(root) if root.is_dir() else path.name),
                'kind': KINDS[suffix], 'extension': suffix, 'bytes': after.st_size,
                'modified_ns': after.st_mtime_ns, 'sha256': digest.hexdigest(),
                'stable_during_hash': (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns)})
        except OSError as exc:
            result['errors'].append({'path': str(path), 'error': str(exc)})

    def visit(path):
        try:
            if linked(path):
                result['skipped_links'].append(str(path))
            elif path.is_dir():
                for child in sorted(path.iterdir(), key=lambda p: p.name.casefold()):
                    visit(child)
            elif path.is_file():
                add_file(path)
        except OSError as exc:
            result['errors'].append({'path': str(path), 'error': str(exc)})

    visit(root)
    groups = {}
    for entry in result['files']:
        groups.setdefault(entry['sha256'], []).append(entry['path'])
    result['identical_content_groups'] = [paths for paths in groups.values() if len(paths) > 1]
    result['counts'] = {kind: sum(f['kind'] == kind for f in result['files']) for kind in ('cad', 'pdf', 'image')}
    result['has_issues'] = bool(result['errors'] or result['skipped_links']
                              or any(not f['stable_during_hash'] for f in result['files']))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', help='Drawing folder or individual file')
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    result = inventory(args.source)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result.get('errors') else 0


if __name__ == '__main__':
    raise SystemExit(main())
