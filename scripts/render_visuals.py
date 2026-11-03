"""Render the repository SVGs to PNG. Optional documentation-only dependency: Playwright."""
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", help="Optional local Chromium/Chrome executable")
    args = parser.parse_args()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, **({"executable_path":args.browser} if args.browser else {}))
        try:
            page = browser.new_page(device_scale_factor=1)
            for source in sorted((ROOT/"docs/images").glob("*.svg")):
                tree = ET.parse(source).getroot()
                width, height = int(tree.attrib["width"]), int(tree.attrib["height"])
                page.set_viewport_size({"width":width,"height":height})
                page.goto(source.as_uri(), wait_until="load")
                page.evaluate("document.fonts.ready")
                overflows = page.locator("text").evaluate_all("els => els.filter(e => {const r=e.getBoundingClientRect();return r.left < -1 || r.right > innerWidth+1 || r.top < -1 || r.bottom > innerHeight+1}).map(e=>e.textContent)")
                if overflows:
                    raise ValueError(f"Text outside canvas in {source.name}: {overflows}")
                page.screenshot(path=str(source.with_suffix(".png")))
                print(f"Rendered {source.name}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
