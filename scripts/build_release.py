"""Build a minimal, portable skill archive with its license and attribution."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/"skills/use-agentsmd"


def main():
    dest=ROOT/"dist/use-agentsmd.zip"
    dest.parent.mkdir(exist_ok=True)
    with ZipFile(dest,"w",ZIP_DEFLATED) as archive:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file(): archive.write(path,Path("use-agentsmd")/path.relative_to(SKILL))
        for name in ["LICENSE","NOTICE.md"]:
            if not (SKILL/name).exists():
                archive.write(ROOT/name,Path("use-agentsmd")/name)
    with ZipFile(dest) as archive:
        if archive.testzip() is not None: raise ValueError("Archive integrity check failed")
        print("Archive contents:",", ".join(archive.namelist()))
    print(f"Built {dest}")


if __name__=="__main__": main()
