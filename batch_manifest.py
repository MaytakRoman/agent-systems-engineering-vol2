from pathlib import Path
from hashlib import sha256
import json
import platform

names = ("batch_before.py", "batch_after.py",
         "batch_checks.py", "batch_properties.py")
def build_manifest():
    files = {}
    for name in sorted(names):
        digest = sha256(Path(name).read_bytes()).hexdigest()
        files[name] = digest
    return {
        "python": platform.python_version(),
        "files": files,
        "command": ["python", "batch_checks.py"],
    }

first = build_manifest()
assert first == build_manifest()
Path("case_manifest.json").write_text(
    json.dumps(first, sort_keys=True, indent=2))
print(f'Манифест: исходных файлов – {len(first["files"])}')
