#!/usr/bin/env python3
"""Build the paper: Markdown sections -> HTML -> PDF via headless Chrome.

Usage:
    python3 paper/build/build.py [--no-pdf]

Design goals:
  * deterministic, dependency-free (stdlib only)
  * numbered citations resolved from refs/refs.bib in order of first appearance
  * figures referenced as [[FIG:path|caption]]
  * raw HTML passthrough for equations/tables that need fine control
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # agent-incentive/
PAPER = ROOT / "paper"
BIB = ROOT / "refs" / "refs.bib"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SECTIONS = [
    "00_frontmatter.md",
    "01_intro.md",
    "02_related.md",
    "03_model.md",
    "04_theory.md",
    "05_architecture.md",
    "06_benchmark.md",
    "07_experiments.md",
    "08_discussion.md",
    "09_conclusion.md",
    "10_appendix.md",
]

# --------------------------------------------------------------------------
# Minimal BibTeX parser (balanced-brace aware)
# --------------------------------------------------------------------------

def parse_bib(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries: dict[str, dict[str, str]] = {}
    i = 0
    n = len(text)
    while i < n:
        at = text.find("@", i)
        if at < 0:
            break
        m = re.match(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text[at:])
        if not m:
            i = at + 1
            continue
        etype, key = m.group(1).lower(), m.group(2)
        j = at + m.end()
        depth = 1
        start = j
        while j < n and depth > 0:
            ch = text[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            j += 1
        body = text[start:j - 1]
        fields: dict[str, str] = {}
        # split top-level commas
        parts, depth, cur = [], 0, []
        for ch in body:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            if ch == "," and depth == 0:
                parts.append("".join(cur))
                cur = []
            else:
                cur.append(ch)
        parts.append("".join(cur))
        for part in parts:
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            k = k.strip().lower()
            v = v.strip()
            if v.startswith("{") and v.endswith("}"):
                v = v[1:-1]
            v = v.replace("\n", " ").strip()
            fields[k] = v
        entries[key] = {"type": etype, **fields}
        i = j
    return entries



ACCENT_MAP = {
    "a": "ä", "e": "ë", "i": "ï", "o": "ö", "u": "ü", "y": "ÿ",
    "A": "Ä", "E": "Ë", "I": "Ï", "O": "Ö", "U": "Ü",
}
ACUTE_MAP = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú",
             "A": "Á", "E": "É", "I": "Í", "O": "Ó", "U": "Ú"}
GRAVE_MAP = {"a": "à", "e": "è", "i": "ì", "o": "ò", "u": "ù"}
CED_MAP = {"c": "ç", "C": "Ç"}


def _detex(s: str) -> str:
    s = re.sub(r'\\"\{?([A-Za-z])\}?', lambda m: ACCENT_MAP.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\\'\{?([A-Za-z])\}?", lambda m: ACUTE_MAP.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\\`\{?([A-Za-z])\}?", lambda m: GRAVE_MAP.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\\c\{?([A-Za-z])\}?", lambda m: CED_MAP.get(m.group(1), m.group(1)), s)
    s = s.replace(r"\aa", "å").replace(r"\AA", "Å").replace(r"\o", "ø").replace(r"\O", "Ø")
    return s

def _plain(s: str) -> str:
    s = _detex(s)
    return re.sub(r"[{}]", "", s)


def format_authors(raw: str) -> str:
    raw = _plain(raw)
    authors = [a.strip() for a in raw.split(" and ") if a.strip()]
    out = []
    for a in authors:
        if "," in a:
            last, first = [x.strip() for x in a.split(",", 1)]
            first = first.replace("'", "").replace("\u2019", "")
            toks = []
            for p in first.split():
                if p.endswith("."):
                    toks.append(p if len(p) <= 2 else p[0] + ".")
                else:
                    toks.append(p[0] + ".")
            initials = " ".join(toks)
            out.append(f"{initials} {last}")
        else:
            out.append(a)
    if len(out) > 4:
        return ", ".join(out[:3]) + ", et al."
    if len(out) == 1:
        return out[0]
    if len(out) == 2:
        return out[0] + " and " + out[1]
    return ", ".join(out[:-1]) + ", and " + out[-1]


def format_ref(key: str, e: dict[str, str]) -> str:
    title = _plain(e.get("title", key)).replace("``", "\u201c").replace("''", "\u201d").replace("`", "").replace("'", "")
    title = html.escape(title)
    authors = html.escape(format_authors(e.get("author", "")))
    year = html.escape(_plain(e.get("year", "")))
    t = e["type"]
    bits = [f"{authors}{'' if authors.endswith('.') else '.'} <i>{title}</i>."]
    if t == "article":
        venue = _plain(e.get("journal", ""))
        if not venue or "arxiv" in venue.lower():
            eprint = e.get("eprint", "")
            if eprint:
                venue = f"arXiv preprint arXiv:{eprint}"
        bits.append(html.escape(venue) + (f", {year}." if year else "."))
    elif t in ("inproceedings", "conference"):
        bits.append("In " + html.escape(_plain(e.get("booktitle", ""))) + (f", {year}." if year else "."))
    elif t == "book":
        bits.append(html.escape(_plain(e.get("publisher", ""))) + (f", {year}." if year else "."))
    else:
        bits.append((f"{year}." if year else ""))
    doi = e.get("doi", "")
    url = e.get("url", "")
    tail = []
    if doi and "arxiv" not in doi.lower():
        tail.append(f"doi:{html.escape(doi)}")
    elif url:
        tail.append(html.escape(url))
    if tail:
        bits.append(" ".join(tail))
    return " ".join(b for b in bits if b).strip()


# --------------------------------------------------------------------------
# Markdown -> HTML (purpose-built subset)
# --------------------------------------------------------------------------

CITE_RE = re.compile(r"\[((?:@[\w:.\-]+\s*;?\s*)+)\]")

GREEK = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ", r"\Delta": "Δ",
    r"\epsilon": "ε", r"\varepsilon": "ε", r"\zeta": "ζ", r"\eta": "η", r"\theta": "θ",
    r"\Theta": "Θ", r"\kappa": "κ", r"\lambda": "λ", r"\Lambda": "Λ", r"\mu": "μ",
    r"\nu": "ν", r"\xi": "ξ", r"\pi": "π", r"\Pi": "Π", r"\rho": "ρ", r"\sigma": "σ",
    r"\Sigma": "Σ", r"\tau": "τ", r"\upsilon": "υ", r"\phi": "φ", r"\varphi": "φ",
    r"\chi": "χ", r"\psi": "ψ", r"\Psi": "Ψ", r"\omega": "ω", r"\Omega": "Ω",
}
SYMBOLS = {
    r"\in": "∈", r"\notin": "∉", r"\subseteq": "⊆", r"\subset": "⊂", r"\cup": "∪",
    r"\cap": "∩", r"\le": "≤", r"\leq": "≤", r"\ge": "≥", r"\geq": "≥", r"\ne": "≠",
    r"\neq": "≠", r"\to": "→", r"\rightarrow": "→", r"\leftarrow": "←",
    r"\times": "×", r"\cdot": "·", r"\pm": "±", r"\approx": "≈", r"\equiv": "≡",
    r"\infty": "∞", r"\partial": "∂", r"\nabla": "∇", r"\sum": "Σ", r"\prod": "Π",
    r"\int": "∫", r"\mid": "|", r"\ldots": "…", r"\dots": "…", r"\cdots": "⋯",
    r"\forall": "∀", r"\exists": "∃", r"\neg": "¬", r"\wedge": "∧", r"\vee": "∨",
    r"\sim": "∼", r"\simeq": "≃", r"\ll": "≪", r"\gg": "≫", r"\succ": "≻", r"\prec": "≺", r"\succeq": "≽", r"\preceq": "≼",
    r"\propto": "∝", r"\perp": "⊥", r"\parallel": "∥", r"\star": "⋆",
    r"\quad": "\u2003", r"\qquad": "\u2003\u2003", r"\;": "\u2009", r"\,": "\u2009", r"\square": "□", r"\blacksquare": "■",
    r"\!": "", r"\ ": " ",
}
BB = {
    r"\mathbb{E}": "𝔼", r"\mathbb{R}": "ℝ", r"\mathbb{N}": "ℕ", r"\mathbb{Z}": "ℤ",
    r"\mathbb{P}": "ℙ", r"\mathcal{X}": "𝒳", r"\mathcal{A}": "𝒜", r"\mathcal{H}": "ℋ",
    r"\mathcal{M}": "ℳ", r"\mathcal{L}": "ℒ",
}


def render_math(tex: str) -> str:
    """Convert a small LaTeX subset used in inline math to HTML."""
    s = tex.strip()
    # accents and escaped symbols
    s = re.sub(r"\\hat\{([^{}]*)\}", "\\1\u0302", s)
    s = re.sub(r"\\bar\{([^{}]*)\}", "\\1\u0304", s)
    s = re.sub(r"\\tilde\{([^{}]*)\}", "\\1\u0303", s)
    s = re.sub(r"\\hat\s+([A-Za-z])", "\\1\u0302", s)
    s = s.replace("\\%", "%")
    # text-mode wrappers first
    s = re.sub(r"\\(?:text|mathrm|operatorname)\{([^{}]*)\}", r"\1", s)
    # common simple fractions
    s = s.replace(r"\tfrac12", "½").replace(r"\frac12", "½")
    s = s.replace(r"\tfrac{1}{2}", "½").replace(r"\frac{1}{2}", "½")
    # fractions
    for _ in range(3):
        s2 = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
        if s2 == s:
            break
        s = s2
    # sub/superscripts while still in TeX form
    s = re.sub(r"_\{([^{}]*)\}", lambda m: "<sub>" + render_math(m.group(1)) + "</sub>", s)
    s = re.sub(r"\^\{([^{}]*)\}", lambda m: "<sup>" + render_math(m.group(1)) + "</sup>", s)
    s = re.sub(r"_(\\[A-Za-z]+)", lambda m: "<sub>" + render_math(m.group(1)) + "</sub>", s)
    s = re.sub(r"\^(\\[A-Za-z]+)", lambda m: "<sup>" + render_math(m.group(1)) + "</sup>", s)
    s = re.sub(r"_([A-Za-z0-9])", r"<sub>\1</sub>", s)
    s = re.sub(r"\^([A-Za-z0-9*])", r"<sup>\1</sup>", s)
    for k, v in sorted({**BB, **GREEK, **SYMBOLS,
                        r"\ell": "ℓ", r"\hbar": "ℏ", r"\Re": "ℜ", r"\Im": "ℑ"}.items(),
                       key=lambda kv: -len(kv[0])):
        s = s.replace(k, v)
    s = s.replace(r"\{", "\uE000").replace(r"\}", "\uE001")
    s = s.replace("{", "").replace("}", "")
    s = s.replace("\uE000", "{").replace("\uE001", "}")
    s = s.replace("\\", "")
    return s


def math_sub(text: str) -> str:
    """Replace $...$ inline math, leaving $$...$$ display blocks untouched."""
    return re.sub(r"(?<!\$)\$([^$]+?)\$(?!\$)", lambda m: render_math(m.group(1)), text)


def inline(text: str) -> str:
    text = math_sub(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def parse_table(lines: list[str]) -> str:
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    sep = rows[1]
    head = rows[0]
    body = rows[2:]
    out = ['<table class="tbl"><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def convert(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    i = 0
    in_list = None  # 'ul' | 'ol'
    while i < len(lines):
        ln = lines[i]
        s = ln.rstrip()

        # fenced code
        if s.startswith("```"):
            lang = s[3:].strip()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append(f'<pre class="code{" " + lang if lang else ""}">' + "\n".join(buf) + "</pre>")
            continue

        # display math block (raw)
        if s.startswith("$$"):
            buf = [s[2:]]
            if not s.endswith("$$") or len(s) <= 2:
                i += 1
                while i < len(lines) and not lines[i].rstrip().endswith("$$"):
                    buf.append(lines[i])
                    i += 1
                if i < len(lines):
                    buf.append(lines[i].rstrip()[:-2])
            else:
                buf = [s[2:-2]]
            i += 1
            out.append('<div class="eq">' + "\n".join(buf) + "</div>")
            continue

        # heading
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            level = len(m.group(1))
            content = inline(m.group(2))
            out.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # page break
        if s.strip() in ("\\newpage", "<!--pagebreak-->"):
            out.append('<div class="pagebreak"></div>')
            i += 1
            continue

        # figure
        m = re.match(r"^\[\[FIG:([^|\]]+)\|(.+)\]\]\s*$", s)
        if m:
            path, cap = m.group(1), inline(m.group(2))
            out.append(f'<figure><img src="{path}" alt="{cap}"><figcaption>{cap}</figcaption></figure>')
            i += 1
            continue

        # raw html block (block-level tags only; inline tags continue as paragraphs)
        if re.match(r"^<(div|table|figure|pre|section|blockquote|ul|ol|h[1-6])\b", s):
            buf = [inline(ln)]
            # collect contiguous raw block until blank line
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#"):
                buf.append(inline(lines[i]))
                i += 1
            out.append("\n".join(buf))
            continue

        # table
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|$", lines[i + 1].strip()):
            buf = [s]
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                buf.append(lines[i].strip())
                i += 1
            html_tbl = parse_table(buf)
            if out and out[-1].startswith('<div class="tblcap">'):
                cap = out.pop()
                out.append(f'<div class="tblwrap">{cap}{html_tbl}</div>')
            else:
                out.append(html_tbl)
            continue

        # blockquote
        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "<br>".join(inline(x) for x in buf) + "</blockquote>")
            continue

        # lists
        m = re.match(r"^(\s*)[-*]\s+(.*)$", ln)
        if m:
            if in_list != "ul":
                if in_list:
                    out.append(f"</{in_list}>")
                out.append("<ul>")
                in_list = "ul"
            out.append(f"<li>{inline(m.group(2))}</li>")
            i += 1
            continue
        m = re.match(r"^(\s*)\d+\.\s+(.*)$", ln)
        if m:
            if in_list != "ol":
                if in_list:
                    out.append(f"</{in_list}>")
                out.append("<ol>")
                in_list = "ol"
            out.append(f"<li>{inline(m.group(2))}</li>")
            i += 1
            continue

        if in_list:
            out.append(f"</{in_list}>")
            in_list = None

        # blank
        if not s.strip():
            i += 1
            continue

        # paragraph (join soft-wrapped lines)
        buf = [s.strip()]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if (not nxt.strip() or nxt.startswith("#") or nxt.startswith("|")
                    or nxt.startswith(">") or nxt.startswith("```") or nxt.startswith("$$")
                    or re.match(r"^\s*[-*]\s+", nxt) or re.match(r"^\s*\d+\.\s+", nxt)
                    or nxt.startswith("[[FIG:") or nxt.strip() in ("\\newpage", "<!--pagebreak-->")):
                break
            buf.append(nxt.strip())
            i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")

    if in_list:
        out.append(f"</{in_list}>")
    return "\n".join(out)


# --------------------------------------------------------------------------
# Citation resolution across the whole document
# --------------------------------------------------------------------------

class CitationDB:
    def __init__(self, entries: dict[str, dict[str, str]]):
        self.entries = entries
        self.order: list[str] = []

    def cite(self, keys: list[str]) -> str:
        nums = []
        for k in keys:
            if k not in self.entries:
                raise KeyError(f"citation key not in refs.bib: {k}")
            if k not in self.order:
                self.order.append(k)
            nums.append(self.order.index(k) + 1)
        return "[" + ", ".join(str(n) for n in nums) + "]"

    def bibliography(self) -> str:
        rows = []
        for idx, key in enumerate(self.order, 1):
            rows.append(f'<div class="ref"><span class="refno">[{idx}]</span> {format_ref(key, self.entries[key])}</div>')
        return "\n".join(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    entries = parse_bib(BIB)
    db = CitationDB(entries)

    body_parts = []
    for name in SECTIONS:
        path = PAPER / "sections" / name
        if not path.exists():
            print(f"  (skip missing section {name})")
            continue
        raw = path.read_text(encoding="utf-8")
        html_body = convert(raw)

        def repl(m: re.Match) -> str:
            keys = re.findall(r"@([\w:.\-]+)", m.group(1))
            return db.cite(keys)

        html_body = CITE_RE.sub(repl, html_body)
        body_parts.append(f'<section id="{name[:-3]}">\n{html_body}\n</section>')

    refs_html = '<section id="references"><h2>References</h2>\n' + db.bibliography() + "\n</section>"
    style = (PAPER / "build" / "style.css").read_text(encoding="utf-8")

    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Verifiable Incentives</title>
<style>{style}</style></head>
<body>
{"".join(body_parts)}
{refs_html}
</body></html>"""

    out_html = PAPER / "main.html"
    out_html.write_text(doc, encoding="utf-8")
    print(f"HTML written: {out_html} ({len(doc)/1024:.1f} KB)")
    print(f"citations: {len(db.order)} entries cited of {len(entries)} in refs.bib")

    if not args.no_pdf:
        pdf = PAPER / "main.pdf"
        cmd = [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
               "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
               "--virtual-time-budget=15000", out_html.as_uri()]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(res.stdout[-2000:])
            print(res.stderr[-2000:])
            return 1
        data = pdf.read_bytes()
        pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
        print(f"PDF written: {pdf} ({len(data)/1024:.0f} KB, ~{pages} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
