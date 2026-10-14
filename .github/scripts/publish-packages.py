"""Only distributes validated binaries. No application sources or credentials."""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile
import urllib.parse
import zipfile

repo = 'bunajianke/remote-fit'
tag = os.environ['RELEASE_TAG']
assert re.fullmatch(r'v\d+\.\d+\.\d+', tag)
release = json.loads(subprocess.check_output(['gh','release','view',tag,'--repo',repo,'--json','isDraft']))
assert release['isDraft'], 'Uploads must target a draft release'
allowed = {'.exe','.zip','.nupkg','.json','.sha256'}
with tempfile.TemporaryDirectory(prefix='remote-fit-downloads-') as directory:
    stage = pathlib.Path(directory)
    uploads = []
    names = set()
    for arch in ('X64','ARM64'):
        url = os.environ['ARTIFACT_' + arch]
        host = urllib.parse.urlparse(url)
        assert host.scheme == 'https' and host.hostname.endswith('.blob.core.windows.net')
        archive = stage / (arch + '.zip')
        subprocess.run(['curl','--fail','--silent','--show-error','--location','--retry','3',
            '--connect-timeout','30','--max-time','300','--output',str(archive),url], check=True)
        folder = stage / arch
        folder.mkdir()
        with zipfile.ZipFile(archive) as packaged:
            for entry in packaged.infolist():
                path = pathlib.PurePosixPath(entry.filename)
                assert len(path.parts) == 1 and entry.file_size < 300_000_000
                if path.suffix not in allowed: continue
                assert path.name not in names, 'Cross-architecture filename collision'
                names.add(path.name)
                packaged.extract(entry, folder)
        files = list(folder.iterdir())
        assert any(p.suffix == '.exe' for p in files) and any(p.suffix == '.nupkg' for p in files)
        for path in files:
            if path.suffix in {'.exe','.zip','.nupkg'}:
                checksum = pathlib.Path(str(path)+'.sha256')
                assert checksum.exists(), 'Missing checksum: ' + path.name
                expected = checksum.read_text(encoding='utf-8-sig').strip().split()[0]
                assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'Checksum mismatch: ' + path.name
        feed = folder / ('releases.win-' + arch.lower() + '.json')
        manifest = json.loads(feed.read_text())
        assets = manifest['Assets']
        assert assets
        for asset in assets:
            path = folder / asset['FileName']
            assert path.name == asset['FileName'] and path.exists()
            assert path.stat().st_size == asset['Size']
            assert asset['Version'] == tag[1:]
            if asset.get('SHA256'): assert hashlib.sha256(path.read_bytes()).hexdigest().upper() == asset['SHA256'].upper()
        print('Validated', arch, len(files), 'download assets', flush=True)
        uploads.extend(str(path) for path in files)
    subprocess.run(['gh','release','upload',tag,'--repo',repo,'--clobber',*uploads], check=True)
    print('Uploaded verified packages to draft release', tag)
