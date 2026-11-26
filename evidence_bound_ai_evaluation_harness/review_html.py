"""Render a check_packet result as a standalone, read-only review document."""

from html import escape
from typing import Optional


_REASONS = {
    "status_match": (
        "所有引用來源都記載了相同的就診、牙位及拍攝狀態，與陳述一致。",
        "Every cited note agrees with the claim on the visit, tooth and imaging status.",
    ),
    "status_mismatch": (
        "陳述與引用來源記載的拍攝狀態不同。",
        "The claim gives a different imaging status from the cited notes.",
    ),
    "no_citation": (
        "這項陳述沒有列出引用來源。",
        "The claim lists no source to check.",
    ),
    "unknown_citation": (
        "至少一個引用的來源編號在這份資料中找不到。",
        "At least one cited source ID is missing from the packet.",
    ),
    "unrecognized_claim": (
        "核對工具無法從陳述的句型辨識牙位與拍攝狀態。",
        "The checker could not read the tooth and imaging status from the claim’s wording.",
    ),
    "unrecognized_source": (
        "核對工具無法從至少一筆引用來源的句型辨識牙位與拍攝狀態。",
        "The checker could not read the tooth and imaging status from at least one cited note.",
    ),
    "visit_mismatch": (
        "至少一筆引用來源的就診編號與陳述不同。",
        "At least one cited note belongs to a different visit from the claim.",
    ),
    "event_mismatch": (
        "至少一筆引用來源所指的根尖片牙位與陳述不同。",
        "At least one cited note describes a periapical image of a different tooth.",
    ),
    "conflicting_sources": (
        "引用來源對同次就診、同一牙位的拍攝狀態有不同記載。",
        "The cited notes give different imaging statuses for the same tooth and visit.",
    ),
}
_STATES = {
    "planned": ("計畫拍攝", "Planned"),
    "completed": ("已拍攝", "Completed"),
    "not_done": ("尚未拍攝", "Not taken"),
    "unknown": ("完成與否未記載", "Completion undocumented"),
}
_STATUSES = {
    "needs_review": ("需覆核", "Needs review"),
    "matched": ("紀錄相符", "Matched"),
}

_STYLES = """
* { box-sizing: border-box; }
html { color-scheme: light; }
body {
  margin: 0; background: #f5f5f0; color: #192d30; font: 1rem/1.55
    "Source Sans 3", "Noto Sans TC", "PingFang TC", system-ui, sans-serif;
  overflow-wrap: anywhere;
}
main { max-width: 58rem; margin: 0 auto; padding: 2.5rem clamp(1rem, 4vw, 3rem) 4rem; }
header { padding: 1.3rem 0 1.1rem; border-top: 4px solid #27615a; }
h1, h2, h3, p { margin: 0; }
h1 { font-size: clamp(1.8rem, 4vw, 2.65rem); line-height: 1.2; }
h1 [lang=en] { display: block; margin-top: .3rem; font-size: .57em; font-weight: 500; }
header p { margin-top: .9rem; color: #405659; }
nav { display: flex; flex-wrap: wrap; align-items: center; gap: .6rem; }
nav a { padding: .5rem .8rem; border: 1px solid #8b9c97; border-radius: .4rem;
  background: white; color: #194c46; font-weight: 600; text-underline-offset: .16em; }
nav a:hover, summary:hover { background: #edf3ef; }
nav strong { margin-left: .45rem; }
nav > span { margin-inline-start: auto; color: #405659; }
:focus-visible { outline: 3px solid #206499; outline-offset: 2px; }
section { margin-top: 2.1rem; }
h2 { font-size: 1.3rem; margin-bottom: .6rem; }
.english { margin-inline-start: .35em; font-weight: normal; }
details { margin: .65rem 0; background: white; border: 1px solid #bac7c0; border-radius: .5rem; }
details.needs_review { border-inline-start: .25rem solid #975415; }
summary { padding: .85rem 1rem; cursor: pointer; border-radius: .45rem; }
summary::marker { color: #42645c; }
.meta { font-size: .9rem; color: #384d50; }
.meta > span { display: inline-block; margin-inline-end: .85rem; }
.claim-text { display: block; margin: .4rem 0 0; font-size: 1.12rem; font-weight: 650; }
.original { white-space: pre-wrap; }
.body { padding: .8rem 1rem 1.1rem; border-top: 1px solid #dce3df; }
code { font: .9em "IBM Plex Mono", ui-monospace, monospace; }
.event { margin: .3rem 0 .65rem; color: #384d50; font-size: .92rem; }
.reason { margin: .7rem 0 1rem; padding: .65rem .8rem; background: #eef3ef; border-radius: .3rem; }
.reason p[lang=en] { color: #384d50; }
.reason code { display: block; margin-top: .3rem; color: #435a56; }
h3 { font-size: 1rem; }
ul { list-style: none; margin: .45rem 0 0; padding: 0; }
li { border-inline-start: 2px solid #9bafa8; margin-top: .65rem; padding-inline-start: .75rem; }
li .original { margin-top: .15rem; }
@media (max-width: 36rem) {
  main { padding-top: 1rem; }
  nav > span { width: 100%; margin: 0; }
  section { margin-top: 1.5rem; }
}
@media print {
  @page { margin: 15mm; }
  body { background: white; color: black; font-size: 10pt; }
  main { max-width: none; margin: 0; padding: 0; }
  header { padding: .5rem 0; } nav a { display: none; } nav > span { margin: 0; }
  h2, h3, summary { break-after: avoid; }
  details::details-content { content-visibility: visible; display: block; }
  details, details.needs_review { border: 0; border-top: 1px solid #999; border-radius: 0; }
  summary { display: block; padding: .6rem 0; }
  .body { padding: 0 0 .8rem; border: 0; }
  .reason { padding: 0; background: transparent; }
  li { break-inside: avoid; }
}
"""


def _label(zh: str, en: str) -> str:
    """Combine static translations and identify English for screen readers."""
    return f'{zh} <span class="english" lang="en">{en}</span>'


def _field(zh: str, en: str, value: str) -> str:
    return f'<span>{_label(zh, en)} <code><bdi>{escape(value)}</bdi></code></span>'


def _event(event: Optional[dict]) -> str:
    if event is None:
        content = _label("無法辨識句型", "Wording unrecognized")
    else:
        state = event["state"]
        content = (
            f'<code>{escape(event["key"])}</code> · {_label(*_STATES[state])} '
            f'(<code>{escape(state)}</code>)'
        )
    return f'<p class="event">{_label("辨識結果", "Parsed event")} · {content}</p>'


def _evidence(source: dict) -> str:
    source_id = _field("來源", "Source", source["id"])
    if not source["found"]:
        return (
            f'<li><p class="meta">{source_id}</p>'
            f'<p>{_label("找不到此來源", "Source not found")}</p></li>'
        )
    visit = _field("就診", "Visit", source["visit"])
    return (
        f'<li><p class="meta">{source_id} {visit}</p>'
        f'<p class="original" dir="auto">{escape(source["text"])}</p>'
        f'{_event(source["event"])}</li>'
    )


def _claim(row: dict) -> str:
    status, reason = row["status"], row["reason"]
    zh, en = _REASONS[reason]
    opened = " open" if status == "needs_review" else ""
    sources = "".join(_evidence(item) for item in row["evidence"])
    evidence = f"<ul>{sources}</ul>" if sources else f'<p>{_label("未列引用來源", "No sources cited")}</p>'
    return f"""
<details class="{escape(status)}"{opened}>
  <summary>
    <span class="meta">
      {_field("陳述", "Claim", row["claim_id"])} {_field("就診", "Visit", row["visit"])}
      <span>{_label(*_STATUSES[status])}</span>
    </span>
    <span class="claim-text original" dir="auto">{escape(row["text"])}</span>
  </summary>
  <div class="body">
    {_event(row["event"])}
    <div class="reason">
      <h3>{_label("核對原因", "Reason")}</h3><p>{zh}</p><p lang="en">{en}</p>
      <code>{escape(reason)}</code>
    </div>
    <h3>{_label("引用來源", "Cited sources")}</h3>{evidence}
  </div>
</details>"""


def render_review(result: dict) -> str:
    """Present the existing outcomes, preserving claim order within each status."""
    summary = result["summary"]
    groups = {status: [] for status in _STATUSES}
    for row in result["results"]:
        groups[row["status"]].append(_claim(row))
    links, sections = [], []
    for status, rows in groups.items():
        label = _label(*_STATUSES[status])
        links.append(f'<a href="#{status}">{label}<strong>{summary[status]}</strong></a>')
        content = "".join(rows) or f'<p>{_label("此類別沒有陳述", "No claims in this group")}</p>'
        sections.append(f'<section id="{status}"><h2>{label}</h2>{content}</section>')
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>根尖片紀錄核對 · Imaging status review</title>
  <style>{_STYLES}</style>
</head>
<body><main>
  <header><h1>根尖片紀錄核對 <span lang="en">Imaging status review</span></h1>
    <p>本報告以合成資料核對陳述與引用紀錄中的就診、牙位及拍攝狀態。<br>
    <span lang="en">This synthetic document comparison checks each claim against its cited notes for the visit, tooth and documented imaging status.</span></p>
  </header>
  <nav aria-label="按結果瀏覽 · Browse by outcome">{" ".join(links)}
    <span>{_label("陳述總數", "Total claims")} <strong>{summary["total"]}</strong></span>
  </nav>
  {"".join(sections)}
</main></body></html>
"""
