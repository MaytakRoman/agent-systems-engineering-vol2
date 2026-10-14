from pathlib import Path
from tempfile import TemporaryDirectory

def allowed_path(root, relative):
    root = root.resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError('Вне рабочей области')
    return target

with TemporaryDirectory() as directory:
    root = Path(directory) / "work"
    root.mkdir()
    target = allowed_path(root, "src/result.txt")
    assert target == root.resolve() / "src" / "result.txt"
    try:
        allowed_path(root, "../other/result.txt")
    except ValueError:
        print('Внутренний путь принят; выход отклонён')
    else:
        raise AssertionError('Путь вышел за корень')
