"""Check package structure and documentation artifacts using Python's standard library."""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/use-agentsmd"


def check():
    errors=[]
    required=["README.md","README.en.md","LICENSE","NOTICE.md","CONTRIBUTING.md","CHANGELOG.md",
              "skills/use-agentsmd/SKILL.md","skills/use-agentsmd/agents/openai.yaml",
              "skills/use-agentsmd/references/agentsmd-content-guide.md"]
    for rel in required:
        if not (ROOT/rel).is_file(): errors.append(f"Missing {rel}")
    if errors: return errors
    text=(SKILL/"SKILL.md").read_text(encoding="utf-8")
    match=re.match(r"\A---\n(.*?)\n---\n",text,re.S)
    if not match:
        errors.append("SKILL.md needs YAML frontmatter")
    else:
        front=match.group(1)
        name=re.search(r"^name: (.+)$",front,re.M)
        if not name or name.group(1)!=SKILL.name: errors.append("Skill name must match package folder")
        if not re.search(r"^description: \S.+$",front,re.M): errors.append("Missing single-line description")
    ui=(SKILL/"agents/openai.yaml").read_text(encoding="utf-8")
    if 'display_name: "use-agentsmd"' not in ui: errors.append("UI name mismatch")
    md_files=[p for p in ROOT.rglob("*.md") if not any(part in {".git",".preview","dist",".venv"} for part in p.relative_to(ROOT).parts)]
    checked=0
    for path in md_files:
        body=path.read_text(encoding="utf-8")
        # Only prose links are checked. Inline code examples are not artifacts.
        body=re.sub(r"^```.*?^```\s*$","",body,flags=re.M|re.S)
        targets=re.findall(r"\]\(([^\s)]+)(?:\s+[^)]*)?\)",body)
        targets+=re.findall(r'(?:src|href)="([^"]+)"',body)
        for raw in targets:
            target=urlsplit(raw)
            if target.scheme or raw.startswith("#") or not target.path: continue
            resolved=(path.parent/unquote(target.path)).resolve()
            checked+=1
            if not resolved.is_relative_to(ROOT): errors.append(f"Link escapes repository: {path.name}: {raw}")
            elif not resolved.exists(): errors.append(f"Broken local link: {path.relative_to(ROOT)}: {raw}")
    images=ROOT/"docs/images"
    for name in ["hero","lifecycle","workflow","before-after","content-filter"]:
        svg,png=images/f"{name}.svg",images/f"{name}.png"
        if not svg.is_file() or not png.is_file():
            errors.append(f"Missing image pair: {name}"); continue
        try:
            doc=ET.parse(svg).getroot()
            if not any(e.tag.endswith("title") and e.text for e in doc): errors.append(f"Missing SVG title: {name}")
        except ET.ParseError as exc: errors.append(f"Invalid SVG {name}: {exc}")
        if png.read_bytes()[:8]!=b"\x89PNG\r\n\x1a\n": errors.append(f"Invalid PNG signature: {name}")
    for path in SKILL.rglob("*"):
        if path.is_file():
            content=path.read_text(encoding="utf-8")
            if "[TODO:" in content: errors.append(f"Unfinished template: {path.name}")
            if re.search(r"[A-Za-z]:[\\/]Users[\\/]",content): errors.append(f"Personal absolute path: {path.name}")
    if not errors: print(f"OK: skill metadata, {checked} local links, 5 SVG/PNG image pairs, and required release files")
    return errors


if __name__ == "__main__":
    failures=check()
    for failure in failures: print(f"ERROR: {failure}",file=sys.stderr)
    sys.exit(bool(failures))
