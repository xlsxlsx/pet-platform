import re
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
WEB_ROOT = PROJECT_ROOT / "web"


def test_web_asset_references_exist() -> None:
    referenced_assets: set[str] = set()
    for relative_file in ("index.html", "app.js", "styles.css"):
        content = (WEB_ROOT / relative_file).read_text(encoding="utf-8")
        referenced_assets.update(re.findall(r"[\"'(](?:\./)?(assets/[^\"')]+)", content))

    assert referenced_assets
    missing = [asset for asset in sorted(referenced_assets) if not (WEB_ROOT / asset).is_file()]
    assert missing == []


def test_web_app_javascript_syntax() -> None:
    result = subprocess.run(
        ["node", "--check", str(WEB_ROOT / "app.js")],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr or result.stdout
