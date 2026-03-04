from pathlib import Path

path = Path("/tmp/Stained-Glass-Odyssey-Endless/frontend/src/lib/assets/characters/luna")
print(f"Checking {path}")
if path.exists():
    print("Path exists")
    print(f"Is dir: {path.is_dir()}")
    files = list(path.glob("*"))
    print(f"All files: {files}")
    pngs = list(path.glob("*.png"))
    print(f"Pngs: {pngs}")
else:
    print("Path does not exist")
