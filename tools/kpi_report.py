from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"
HTML = OUT / "html"
COV_HTML = OUT / "coverage_html"


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, shell=False)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_pytest_coverage(text: str) -> dict:
    # Looks for TOTAL row in coverage table
    # Example: TOTAL  193  10  95%
    cov = None
    tests = None
    for line in text.splitlines():
        if line.strip().startswith("TOTAL"):
            parts = line.split()
            # TOTAL Stmts Miss Cover
            if len(parts) >= 4:
                cov = parts[3]  # e.g. 95%
        if "passed" in line and "in" in line:
            # e.g. "68 passed in 0.28s"
            tests = line.strip()
    return {"coverage_total": cov, "tests": tests}


def parse_interrogate(text: str) -> str | None:
    # RESULT: PASSED (minimum: 80.0%, actual: 98.9%)
    for line in text.splitlines():
        if "actual:" in line:
            return line.strip()
    return None


def parse_mypy_errors(text: str) -> int:
    # Found X errors in Y files
    for line in text.splitlines():
        if line.strip().startswith("Found ") and " errors" in line:
            # Found 7 errors in 2 files ...
            try:
                return int(line.split()[1])
            except Exception:
                return -1
    # If "Success: no issues found"
    if "Success: no issues found" in text:
        return 0
    return -1


def parse_radon_cc_find_worst(text: str) -> tuple[str | None, str | None]:
    # Find highest grade like "C (16)" etc. We take first occurrence of C/D/E/F with largest number.
    worst = None
    worst_line = None
    for line in text.splitlines():
        if " - " not in line:
            continue
        # example: "F 21:0 play - C (16)"
        if "(" in line and ")" in line:
            try:
                grade = line.split(" - ")[-1].split()[0]  # C
                score_str = line.split("(")[-1].split(")")[0]  # 16
                score = int(score_str)
                if worst is None or score > worst:
                    worst = score
                    worst_line = line.strip()
            except Exception:
                pass
    return (str(worst) if worst is not None else None, worst_line)


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def make_summary_html(data: dict) -> str:
    rows = [
        ("Tests", data.get("tests", "")),
        ("Coverage (core+cli)", data.get("coverage_total", "")),
        ("Ruff", data.get("ruff_status", "")),
        ("Interrogate (docs)", data.get("interrogate", "")),
        ("MyPy errors", str(data.get("mypy_errors", ""))),
        ("Radon worst CC", f"{data.get('radon_worst_cc','')} | {data.get('radon_worst_line','')}"),
        ("Generated", data.get("generated_at", "")),
    ]
    tr = "\n".join(
        f"<tr><th>{html_escape(k)}</th><td><pre style='margin:0;white-space:pre-wrap'>{html_escape(v)}</pre></td></tr>"
        for k, v in rows
    )

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Mastermind KPI Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    h1 {{ margin: 0 0 12px 0; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 10px; vertical-align: top; text-align: left; }}
    th {{ width: 220px; background: #f7f7f7; }}
    .links a {{ margin-right: 14px; }}
    code {{ background: #f2f2f2; padding: 2px 6px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>Mastermind KPI Report</h1>
  <p class="links">
    <a href="../coverage_html/index.html">Coverage HTML</a>
    <a href="pytest.txt">pytest output</a>
    <a href="ruff.txt">ruff output</a>
    <a href="mypy.txt">mypy output</a>
    <a href="radon_cc.txt">radon cc output</a>
    <a href="radon_raw.txt">radon raw output</a>
    <a href="interrogate.txt">interrogate output</a>
    <a href="kpi.json">kpi.json</a>
  </p>
  <table>
    {tr}
  </table>
</body>
</html>"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    HTML.mkdir(parents=True, exist_ok=True)

    data: dict = {}
    data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S %z")

    # 1) Ruff
    rc, out = run(["ruff", "check", "src", "tests"])
    write_text(HTML / "ruff.txt", out)
    data["ruff_status"] = "PASS" if rc == 0 else f"FAIL (code={rc})"

    # 2) Interrogate
    rc_i, out_i = run(["interrogate", "src/mastermind"])
    write_text(HTML / "interrogate.txt", out_i)
    data["interrogate"] = parse_interrogate(out_i) or ("PASS" if rc_i == 0 else "FAIL")

    # 3) Radon
    rc_cc, out_cc = run(["radon", "cc", "src/mastermind", "-s"])
    write_text(HTML / "radon_cc.txt", out_cc)
    worst_cc, worst_line = parse_radon_cc_find_worst(out_cc)
    data["radon_worst_cc"] = worst_cc or ""
    data["radon_worst_line"] = worst_line or ""

    rc_raw, out_raw = run(["radon", "raw", "src/mastermind"])
    write_text(HTML / "radon_raw.txt", out_raw)

    # 4) MyPy (do not fail the report if mypy fails)
    rc_m, out_m = run(["mypy", "src/mastermind"])
    write_text(HTML / "mypy.txt", out_m)
    data["mypy_errors"] = parse_mypy_errors(out_m)

    # 5) Pytest + Coverage HTML
    # Run pytest first (your pyproject addopts handles cov report term-missing)
    rc_p, out_p = run(["pytest"])
    write_text(HTML / "pytest.txt", out_p)
    data.update(parse_pytest_coverage(out_p))

    # Generate coverage HTML (coverage.py reads last run)
    # If pytest failed, this may fail; still attempt.
    _rc_ch, out_ch = run(["coverage", "html", "-d", str(COV_HTML)])
    write_text(HTML / "coverage_html_build.txt", out_ch)

    # Save json + summary html
    write_text(HTML / "kpi.json", json.dumps(data, indent=2))
    write_text(HTML / "index.html", make_summary_html(data))

    print(f"\nKPI report generated:")
    print(f"- Summary: {HTML / 'index.html'}")
    print(f"- Coverage: {COV_HTML / 'index.html'}")
    return 0 if rc_p == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
