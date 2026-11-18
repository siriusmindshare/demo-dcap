"""Create local config and copy only synthetic fixtures. Never overwrite files."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]
for directory in ("_local/input", "_local/output"):
    (ROOT / directory).mkdir(parents=True, exist_ok=True)
for source, target in [
    ("config/paths.example.yaml", "config/paths.local.yaml"),
    ("tests/fixtures/enrollment.csv", "_local/input/enrollment.csv"),
]:
    destination = ROOT / target
    if destination.exists():
        print(f"Kept existing {target}")
    else:
        shutil.copyfile(ROOT / source, destination)
        print(f"Created {target}")
