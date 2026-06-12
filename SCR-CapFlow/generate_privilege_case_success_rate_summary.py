#!/usr/bin/env python3
"""Generate root privilege-amplification success-rate summaries from latest case results."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
CASE_INDEX = ROOT / "case_index.md"
OUT_MD = ROOT / "case_success_rate_summary.md"
OUT_XLSX = ROOT / "case_success_rate_summary.xlsx"
PROGRESS = ROOT / "target-progress.md"
CONDITIONS = ["control", "A_only", "B_only", "A+B_neutral", "A+B_explicit"]
PRESERVED_ALIASES = {
    "mapper_only": "A_only",
    "scheduler_only": "B_only",
    "indexer_only": "A_only",
    "manager_only": "B_only",
    "explorer_only": "A_only",
    "broadcaster_only": "B_only",
}


def fmt_pct(value) -> str:
    if value is None:
        return ""
    pct = round(float(value) * 100, 1)
    if pct.is_integer():
        return str(int(pct))
    return f"{pct:.1f}"


def fmt_float(value) -> str:
    if value is None:
        return ""
    value = round(float(value), 1)
    if value.is_integer():
        return str(int(value))
    return f"{value:.1f}"


def parse_case_index() -> list[dict[str, str]]:
    if not CASE_INDEX.exists():
        return []
    rows: list[dict[str, str]] = []
    for line in CASE_INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| case"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        case_id = cells[0]
        rows.append({
            "case": case_id,
            "case_num": int(case_id.replace("case", "")),
            "status": cells[1],
            "category": cells[2],
            "scenario": cells[3],
            "skill_a": cells[4],
            "skill_b": cells[5],
            "side_effect": cells[6],
        })
    return sorted(rows, key=lambda row: row["case_num"])


def latest_result_file(case_num: int) -> Path | None:
    candidates: list[Path] = []
    result_dir = ROOT / "cases" / f"case{case_num}" / "results"
    if result_dir.exists():
        candidates.extend(result_dir.glob("*.json"))
    legacy_dir = ROOT / "scripts" / "results"
    if legacy_dir.exists():
        candidates.extend(legacy_dir.glob(f"experiment_case{case_num}*.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def condition_rate(payload: dict | None) -> float | None:
    if not isinstance(payload, dict):
        return None
    for key in ["linked_attack_rate", "exposed_rate", "exfil_rate", "dangerous_rate"]:
        if key in payload:
            return float(payload[key])
    trials = payload.get("trials", [])
    if not isinstance(trials, list) or not trials:
        return None
    for key in ["attack_chain_success", "sensitive_exposed", "exfil", "dangerous_action_taken"]:
        if any(key in trial for trial in trials if isinstance(trial, dict)):
            return sum(1 for trial in trials if isinstance(trial, dict) and trial.get(key)) / len(trials)
    return None


def load_case_rates(case_num: int) -> tuple[dict[str, float | None], str]:
    result = latest_result_file(case_num)
    if result is None:
        return {}, "missing result"
    data = load_json(result)
    if not data:
        return {}, f"invalid json: {rel(result)}"
    raw_conditions = data.get("conditions", {})
    if not isinstance(raw_conditions, dict):
        return {}, f"missing conditions: {rel(result)}"

    rates: dict[str, float | None] = {}
    for raw_name, payload in raw_conditions.items():
        name = PRESERVED_ALIASES.get(raw_name, raw_name)
        if name in CONDITIONS:
            rates[name] = condition_rate(payload)
    return rates, rel(result)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def mean(values) -> float | None:
    nums = [float(v) for v in values if v is not None]
    return sum(nums) / len(nums) if nums else None


def md_table(headers: list[str], rows: list[list[object]], numeric_headers: set[str] | None = None) -> str:
    numeric_headers = numeric_headers or set()
    aligns = ["---:" if header in numeric_headers or header.endswith("(%)") else "---" for header in headers]
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(aligns) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def col_name(n: int) -> str:
    name = ""
    while n:
        n, r = divmod(n - 1, 26)
        name = chr(65 + r) + name
    return name


def cell_xml(row_idx: int, col_idx: int, value) -> str:
    ref = f"{col_name(col_idx)}{row_idx}"
    if value is None or value == "":
        return f'<c r="{ref}"/>'
    if isinstance(value, (int, float)):
        return f'<c r="{ref}"><v>{value}</v></c>'
    return f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'


def sheet_xml(rows: list[list[object]]) -> str:
    body = []
    for row_idx, row in enumerate(rows, 1):
        body.append(f'<row r="{row_idx}">' + "".join(cell_xml(row_idx, col_idx, value) for col_idx, value in enumerate(row, 1)) + "</row>")
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheetData>' + "".join(body) + "</sheetData></worksheet>"


def write_xlsx(sheets: list[tuple[str, list[list[object]]]]) -> None:
    content_types = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    for i in range(1, len(sheets) + 1):
        content_types.append(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')
    content_types.append("</Types>")

    workbook_sheets = []
    workbook_rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">']
    for i, (name, _) in enumerate(sheets, 1):
        workbook_sheets.append(f'<sheet name="{escape(name[:31])}" sheetId="{i}" r:id="rId{i}"/>')
        workbook_rels.append(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>')
    workbook_rels.append("</Relationships>")
    workbook_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(workbook_sheets) + "</sheets></workbook>"
    root_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    core = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:creator>Claude Code</dc:creator><cp:lastModifiedBy>Claude Code</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>'
    app = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Claude Code</Application></Properties>'

    with zipfile.ZipFile(OUT_XLSX, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", "".join(content_types))
        zf.writestr("_rels/.rels", root_rels)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", "".join(workbook_rels))
        zf.writestr("docProps/core.xml", core)
        zf.writestr("docProps/app.xml", app)
        for i, (_, rows) in enumerate(sheets, 1):
            zf.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(rows))


def update_progress(missing_count: int) -> None:
    if not PROGRESS.exists():
        return
    text = PROGRESS.read_text(encoding="utf-8")
    text = text.replace("- [ ] Create `case_success_rate_summary.md`", "- [x] Create `case_success_rate_summary.md`")
    text = text.replace("- [ ] Create `case_success_rate_summary.xlsx`", "- [x] Create `case_success_rate_summary.xlsx`")
    note = f"- Generated `{OUT_MD.name}` and `{OUT_XLSX.name}` at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n- Missing result cases: {missing_count}"
    if "## Summary generation" not in text:
        text += "\n## Summary generation\n\n" + note + "\n"
    else:
        text = re.sub(r"## Summary generation\n\n.*", "## Summary generation\n\n" + note + "\n", text, flags=re.S)
    PROGRESS.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-missing", action="store_true", help="Return 0 even if some cases have no result JSON")
    args = parser.parse_args()

    meta = parse_case_index()
    rates_by_case: dict[int, dict[str, float | None]] = {}
    notes: dict[int, str] = {}
    for item in meta:
        rates, note = load_case_rates(item["case_num"])
        rates_by_case[item["case_num"]] = rates
        notes[item["case_num"]] = note

    detail_rows = []
    for item in meta:
        rates = rates_by_case.get(item["case_num"], {})
        detail_rows.append([
            f"`{item['case']}`",
            item["status"],
            item["category"],
            item["scenario"],
            fmt_pct(rates.get("control")),
            fmt_pct(rates.get("A_only")),
            fmt_pct(rates.get("B_only")),
            fmt_pct(rates.get("A+B_neutral")),
            fmt_pct(rates.get("A+B_explicit")),
            notes.get(item["case_num"], ""),
        ])

    family_rows = []
    by_family: dict[str, list[int]] = defaultdict(list)
    for item in meta:
        by_family[item["category"]].append(item["case_num"])
    for family in sorted(by_family):
        nums = by_family[family]
        family_rows.append([
            family,
            len(nums),
            fmt_pct(mean(rates_by_case.get(n, {}).get("control") for n in nums)),
            fmt_pct(mean(rates_by_case.get(n, {}).get("A_only") for n in nums)),
            fmt_pct(mean(rates_by_case.get(n, {}).get("B_only") for n in nums)),
            fmt_pct(mean(rates_by_case.get(n, {}).get("A+B_neutral") for n in nums)),
            fmt_pct(mean(rates_by_case.get(n, {}).get("A+B_explicit") for n in nums)),
        ])

    overall_row = [[
        "Overall mean",
        len(meta),
        fmt_pct(mean(rates_by_case.get(item["case_num"], {}).get("control") for item in meta)),
        fmt_pct(mean(rates_by_case.get(item["case_num"], {}).get("A_only") for item in meta)),
        fmt_pct(mean(rates_by_case.get(item["case_num"], {}).get("B_only") for item in meta)),
        fmt_pct(mean(rates_by_case.get(item["case_num"], {}).get("A+B_neutral") for item in meta)),
        fmt_pct(mean(rates_by_case.get(item["case_num"], {}).get("A+B_explicit") for item in meta)),
    ]]

    metric_headers = ["Group", "Cases", "control (%)", "A_only (%)", "B_only (%)", "A+B_neutral (%)", "A+B_explicit (%)"]
    detail_headers = ["Case", "Status", "Family", "Scenario", "control (%)", "A_only (%)", "B_only (%)", "A+B_neutral (%)", "A+B_explicit (%)", "Result file"]
    numeric_headers = {"Cases", "control (%)", "A_only (%)", "B_only (%)", "A+B_neutral (%)", "A+B_explicit (%)"}

    md = [
        "# Privilege Amplification Case Success Rate Summary",
        "",
        "数据来源：每个 case 的最新 `cases/case*/results/*.json`（兼容旧版 `scripts/results/experiment_case*.json`）。",
        "",
        "成功率优先使用 `linked_attack_rate`；旧版 preserved case 会兼容 `exposed_rate` / `exfil_rate` / `dangerous_rate`。",
        "",
        "## Overall Aggregate",
        "",
        md_table(metric_headers, overall_row, numeric_headers),
        "",
        "## Family Aggregate",
        "",
        md_table(metric_headers, family_rows, numeric_headers),
        "",
        "## Per-case Rates",
        "",
        md_table(detail_headers, detail_rows, numeric_headers),
        "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    x_overall = [metric_headers] + [[cell.strip("`") if isinstance(cell, str) else cell for cell in row] for row in overall_row]
    x_family = [metric_headers] + family_rows
    x_detail = [detail_headers] + [[str(cell).strip("`") for cell in row] for row in detail_rows]
    write_xlsx([("Overall", x_overall), ("Family", x_family), ("Per Case", x_detail)])

    missing = [item["case"] for item in meta if notes.get(item["case_num"]) == "missing result"]
    update_progress(len(missing))
    print(json.dumps({"summary_md": rel(OUT_MD), "summary_xlsx": rel(OUT_XLSX), "cases": len(meta), "missing": missing}, ensure_ascii=False, indent=2))
    return 0 if args.allow_missing or not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
