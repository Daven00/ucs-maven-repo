#!/usr/bin/env python3
"""Generate index.html from the maven-metadata.xml files of the repo."""
import html
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE_URL = "https://daven00.github.io/ucs-maven-repo"
# Maven repositories: (folder, title). Folders that don't exist yet are skipped.
REPOS = [
    ("releases/rest", "REST branch"),
    ("releases/integration", "Integration branch"),
]


def fmt_date(s):
    try:
        return datetime.strptime(s, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M UTC")
    except (TypeError, ValueError):
        return "-"


def artifacts(repo):
    for meta in sorted((ROOT / repo).rglob("maven-metadata.xml")):
        r = ET.parse(meta).getroot()
        gid, aid = r.findtext("groupId"), r.findtext("artifactId")
        versions = [v.text for v in r.findall("./versioning/versions/version")]
        if not (gid and aid and versions):
            continue  # skip group-level / snapshot metadata
        yield {
            "gid": gid,
            "aid": aid,
            "versions": versions,
            "release": r.findtext("./versioning/release") or versions[-1],
            "updated": fmt_date(r.findtext("./versioning/lastUpdated")),
        }


def version_links(repo, a):
    base = f"{repo}/{a['gid'].replace('.', '/')}/{a['aid']}"
    out = []
    for v in reversed(a["versions"]):
        links = [f'<a href="{base}/{v}/{a["aid"]}-{v}.pom">pom</a>']
        if (ROOT / base / v / f"{a['aid']}-{v}.jar").exists():
            links.append(f'<a href="{base}/{v}/{a["aid"]}-{v}.jar">jar</a>')
        out.append(f"{html.escape(v)} ({', '.join(links)})")
    return "<br>".join(out)


parts = ["""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>UCS Maven repository</title>
<style>body{font-family:sans-serif;max-width:60em;margin:2em auto;padding:0 1em}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:.4em;
vertical-align:top;text-align:left}pre{background:#f4f4f4;padding:.8em;overflow-x:auto}</style>
</head><body>
<h1>UCS Maven repository</h1>
<p>Maven artifacts of the Usage Control framework (research code).
Provided for research purposes only, with no warranty and not intended
for production or security-critical use.</p>
<p>Each branch is a separate Maven repository: add only the URL of the one you need.</p>"""]

for repo, title in REPOS:
    arts = list(artifacts(repo))
    if not arts:
        continue
    parts.append(f"<h2>{html.escape(title)}</h2>")
    parts.append(f"<p>Repository URL: <code>{BASE_URL}/{repo}/</code></p>")
    parts.append(
        "<pre>&lt;repositories&gt;\n  &lt;repository&gt;\n"
        "    &lt;id&gt;ucs-public&lt;/id&gt;\n"
        f"    &lt;url&gt;{BASE_URL}/{repo}/&lt;/url&gt;\n"
        "  &lt;/repository&gt;\n&lt;/repositories&gt;</pre>")
    parts.append("<table><tr><th>groupId : artifactId</th><th>Last deployed</th>"
                 "<th>All versions</th></tr>")
    for a in arts:
        parts.append(
            f"<tr><td>{html.escape(a['gid'])}:<b>{html.escape(a['aid'])}</b></td>"
            f"<td>{html.escape(a['release'])}<br><small>{a['updated']}</small></td>"
            f"<td>{version_links(repo, a)}</td></tr>")
    parts.append("</table>")

parts.append("</body></html>")
(ROOT / "index.html").write_text("\n".join(parts), encoding="utf-8")
print("index.html updated")
