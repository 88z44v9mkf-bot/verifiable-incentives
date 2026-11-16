#!/usr/bin/env python3
"""Generate SVG figures for the paper (no plotting libraries)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "paper" / "figures"
FIG.mkdir(exist_ok=True)

FONT = "Times New Roman, Times, serif"
INK = "#222"
MUTED = "#555"


def box(x, y, w, h, lines, fill="#fff", stroke=INK, rx=6, fs=12, bold=False):
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>']
    n = len(lines)
    for i, line in enumerate(lines):
        yy = y + h / 2 + (i - (n - 1) / 2) * (fs + 5) + fs * 0.35
        weight = "bold" if bold and i == 0 else "normal"
        s.append(f'<text x="{x + w/2}" y="{yy:.1f}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" font-weight="{weight}" fill="{INK}">{line}</text>')
    return "".join(s)


def arrow(x1, y1, x2, y2, label="", dash=False, curve=None):
    d = f'M{x1},{y1} L{x2},{y2}' if not curve else curve
    s = [f'<path d="{d}" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arr)"' + (' stroke-dasharray="4 3"' if dash else '') + '/>']
    if label:
        s.append(f'<text x="{(x1+x2)/2}" y="{(y1+y2)/2-5}" text-anchor="middle" font-family="{FONT}" font-size="10.5" fill="{MUTED}">{label}</text>')
    return "".join(s)


def architecture():
    W, H = 920, 470
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    p.append(box(30, 190, 150, 96, ["User", "(principal)", "budget B", "authority C"], fs=12, bold=True))
    p.append(box(240, 40, 190, 86, ["Identity issuer", "(Poppy-like)", "principal, scope,", "expiry, signature"], fs=11.5))
    p.append(box(240, 190, 190, 96, ["Agent runtime", "verify credential", "plan and choose"], fs=12, bold=True))
    p.append(box(500, 190, 190, 96, ["Merchant", "offers", "price, quality,", "action, sponsorship"], fs=11.5))
    p.append(box(760, 190, 130, 96, ["Wallet", "budget,", "one-time card"], fs=11.5))
    p.append(box(470, 350, 190, 84, ["Collusion monitor", "audit hidden", "sponsorship"], fs=11.5))
    p.append(box(760, 350, 130, 84, ["Stake and", "reputation"], fs=11.5))
    p.append(arrow(180, 238, 240, 238, "delegates"))
    p.append(arrow(335, 126, 335, 190, "credential"))
    p.append(arrow(430, 238, 500, 238, "offers"))
    p.append(arrow(690, 238, 760, 238, "payment"))
    p.append(arrow(825, 286, 825, 350, "", dash=True))
    p.append(arrow(660, 392, 760, 392, "", dash=True))
    p.append('<path d="M470,392 L430,392 L430,286" fill="none" stroke="#555" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr)"/>')
    p.append(arrow(760, 238, 600, 350, "", dash=True))
    p.append(f'<text x="460" y="450" text-anchor="middle" font-family="{FONT}" font-size="11" fill="{MUTED}">Solid: task flow. Dashed: payment audit, penalty, and continuation feedback.</text>')
    p.append("</svg>")
    (FIG / "fig_architecture.svg").write_text("".join(p), encoding="utf-8")


def collusion():
    s = json.loads((ROOT / "results" / "summary.json").read_text())
    models = ["deepseek-v4.1-flash-1017", "kimi-k3.1-pro"]
    labels = ["DeepSeek", "Kimi"]
    regs = ["R0", "R1", "R2", "R3", "R4"]
    cell = {(c["model"], c["regime"]): c for c in s["cells"]}
    W, H = 760, 360
    left, bottom, top = 70, 60, 40
    plot_w, plot_h = W - left - 30, H - bottom - top
    ymax = 25.0
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    p.append(f'<line x1="{left}" y1="{H-bottom}" x2="{W-30}" y2="{H-bottom}" stroke="{INK}" stroke-width="1"/>')
    p.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{H-bottom}" stroke="{INK}" stroke-width="1"/>')
    for v in range(0, 26, 5):
        y = H - bottom - v / ymax * plot_h
        p.append(f'<line x1="{left}" y1="{y:.1f}" x2="{W-30}" y2="{y:.1f}" stroke="#e5e5e5" stroke-width="0.8"/>')
        p.append(f'<text x="{left-8}" y="{y+4:.1f}" text-anchor="end" font-family="{FONT}" font-size="11" fill="{MUTED}">{v}%</text>')
    group_w = plot_w / len(regs)
    bw = group_w * 0.28
    colors = ["#3d5a80", "#c26a3a"]
    for gi, reg in enumerate(regs):
        cx = left + group_w * (gi + 0.5)
        p.append(f'<text x="{cx:.1f}" y="{H-bottom+20}" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{INK}">{reg}</text>')
        for mi, (m, lab) in enumerate(zip(models, labels)):
            c = cell[(m, reg)]
            val = c["collusion"] * 100
            lo, hi = [x * 100 for x in c["collusion_ci"]]
            x = cx - bw + mi * (bw + 3)
            y = H - bottom - val / ymax * plot_h
            y0 = H - bottom - hi / ymax * plot_h
            y1 = H - bottom - lo / ymax * plot_h
            p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{H-bottom-y:.1f}" fill="{colors[mi]}" opacity="0.85"/>')
            p.append(f'<line x1="{x+bw/2:.1f}" y1="{y0:.1f}" x2="{x+bw/2:.1f}" y2="{y1:.1f}" stroke="{INK}" stroke-width="1"/>')
            p.append(f'<line x1="{x+bw/2-3:.1f}" y1="{y0:.1f}" x2="{x+bw/2+3:.1f}" y2="{y0:.1f}" stroke="{INK}" stroke-width="1"/>')
            p.append(f'<line x1="{x+bw/2-3:.1f}" y1="{y1:.1f}" x2="{x+bw/2+3:.1f}" y2="{y1:.1f}" stroke="{INK}" stroke-width="1"/>')
    p.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{MUTED}">Delegation regime (R0 none, R1 credential, R2 wallet, R3 audit+disclosure, R4 stake). Bars show mean; whiskers 95% bootstrap CI.</text>')
    # legend
    for mi, (lab, col) in enumerate(zip(labels, colors)):
        lx = left + 10 + mi * 90
        p.append(f'<rect x="{lx}" y="{top-22}" width="12" height="9" fill="{col}"/>')
        p.append(f'<text x="{lx+18}" y="{top-14}" font-family="{FONT}" font-size="11" fill="{INK}">{lab}</text>')
    p.append(f'<text x="{left}" y="{top-32}" font-family="{FONT}" font-size="11.5" fill="{INK}">Collusion rate by regime</text>')
    p.append("</svg>")
    (FIG / "fig_collusion.svg").write_text("".join(p), encoding="utf-8")


def sandbox():
    s = json.loads((ROOT / "results" / "sandbox_summary.json").read_text())
    regs = ["R0", "R2", "R3", "R4"]
    colors = {"R0": "#3d5a80", "R2": "#6b8e9f", "R3": "#c26a3a", "R4": "#8a4b2a"}
    by = {(b["regime"], b["round"]): b for b in s["by_round"]}
    W, H = 760, 330
    pw, ph = 300, 190
    panes = [(60, 70, "Collusion rate"), (460, 70, "Mean balance ($)")]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" fill="#fff"/>']
    for (x0, y0, title), key, ymax in zip(panes, ["collusion", "mean_balance"], [15.0, 100.0]):
        p.append(f'<text x="{x0+pw/2}" y="{y0-22}" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{INK}">{title}</text>')
        p.append(f'<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" stroke="{INK}"/>')
        p.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+ph}" stroke="{INK}"/>')
        for v in range(0, int(ymax)+1, int(ymax//3)):
            yy = y0 + ph - v/ymax*ph
            p.append(f'<text x="{x0-6}" y="{yy+4}" text-anchor="end" font-family="{FONT}" font-size="9.5" fill="{MUTED}">{v}{"%" if key=="collusion" else ""}</text>')
        for rr in range(1, 6):
            xx = x0 + (rr-0.5)/5*pw
            p.append(f'<text x="{xx}" y="{y0+ph+16}" text-anchor="middle" font-family="{FONT}" font-size="10" fill="{MUTED}">{rr}</text>')
        for reg in regs:
            pts = []
            for rr in range(1, 6):
                b = by[(reg, rr)]
                val = b[key] * (100 if key == "collusion" else 1)
                xx = x0 + (rr-0.5)/5*pw
                yy = y0 + ph - val/ymax*ph
                pts.append(f"{xx:.1f},{yy:.1f}")
            p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colors[reg]}" stroke-width="1.6"/>')
            for pt in pts:
                xx, yy = pt.split(",")
                p.append(f'<circle cx="{xx}" cy="{yy}" r="2.2" fill="{colors[reg]}"/>')
    for i, reg in enumerate(regs):
        lx = 60 + i*70
        p.append(f'<rect x="{lx}" y="{H-16}" width="10" height="7" fill="{colors[reg]}"/>')
        p.append(f'<text x="{lx+14}" y="{H-10}" font-family="{FONT}" font-size="10" fill="{INK}">{reg}</text>')
    p.append("</svg>")
    (FIG / "fig_sandbox.svg").write_text("".join(p), encoding="utf-8")


def econ():
    s = json.loads((ROOT / "results" / "summary_econ.json").read_text())
    models = ["deepseek-v4.1-flash-1017", "kimi-k3.1-pro", "qwen3.8-flash"]
    labels = ["DeepSeek", "Kimi", "Qwen-Flash"]
    regs = ["R0", "R2", "R3", "R4"]
    cell = {(c["model"], c["regime"]): c for c in s["cells"]}
    colors = ["#3d5a80", "#c26a3a", "#5b8c5a"]
    W, H = 760, 340
    left, bottom, top = 70, 60, 40
    plot_w, plot_h = W - left - 30, H - bottom - top
    ymax = 60.0
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" fill="#fff"/>']
    p.append(f'<line x1="{left}" y1="{H-bottom}" x2="{W-30}" y2="{H-bottom}" stroke="{INK}"/>')
    p.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{H-bottom}" stroke="{INK}"/>')
    for v in range(0, 61, 10):
        y = H - bottom - v/ymax*plot_h
        p.append(f'<line x1="{left}" y1="{y:.1f}" x2="{W-30}" y2="{y:.1f}" stroke="#e5e5e5"/>')
        p.append(f'<text x="{left-8}" y="{y+4:.1f}" text-anchor="end" font-family="{FONT}" font-size="11" fill="{MUTED}">{v}%</text>')
    gw = plot_w/len(regs); bw = gw*0.22
    for gi, reg in enumerate(regs):
        cx = left + gw*(gi+0.5)
        p.append(f'<text x="{cx:.1f}" y="{H-bottom+20}" text-anchor="middle" font-family="{FONT}" font-size="12">{reg}</text>')
        for mi, m in enumerate(models):
            val = cell[(m, reg)]["collusion"]*100
            x = cx - (bw*1.5) + mi*bw
            y = H - bottom - val/ymax*plot_h
            p.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw-2:.1f}" height="{H-bottom-y:.1f}" fill="{colors[mi]}" opacity="0.9"/>')
    for mi, lab in enumerate(labels):
        lx = left + 10 + mi*100
        p.append(f'<rect x="{lx}" y="{top-22}" width="12" height="9" fill="{colors[mi]}"/>')
        p.append(f'<text x="{lx+18}" y="{top-14}" font-family="{FONT}" font-size="11">{lab}</text>')
    p.append(f'<text x="{left}" y="{top-32}" font-family="{FONT}" font-size="11.5">Collusion rate, own-earnings objective</text>')
    p.append(f'<text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="{FONT}" font-size="10.5" fill="{MUTED}">Regimes R0 (no audit), R2 (wallet), R3 (audit + disclosure), R4 (stake).</text>')
    p.append("</svg>")
    (FIG / "fig_econ.svg").write_text("".join(p), encoding="utf-8")


def econ_sandbox():
    s = json.loads((ROOT / "results" / "summary_econ_sandbox.json").read_text())
    regs = ["R0", "R2", "R3", "R4"]
    colors = {"R0": "#3d5a80", "R2": "#6b8e9f", "R3": "#c26a3a", "R4": "#8a4b2a"}
    by = {(b["regime"], b["round"]): b for b in s["by_round"]}
    W, H = 760, 320
    pw, ph = 300, 190
    panes = [(60, 70, "Collusion rate"), (460, 70, "Mean balance (USD)")]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', f'<rect width="{W}" height="{H}" fill="#fff"/>']
    for (x0, y0, title), key, ymax in zip(panes, ["collusion", "balance"], [40.0, 140.0]):
        p.append(f'<text x="{x0+pw/2}" y="{y0-22}" text-anchor="middle" font-family="{FONT}" font-size="12">{title}</text>')
        p.append(f'<line x1="{x0}" y1="{y0+ph}" x2="{x0+pw}" y2="{y0+ph}" stroke="{INK}"/>')
        p.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+ph}" stroke="{INK}"/>')
        for v in range(0, int(ymax)+1, int(ymax//4)):
            yy = y0 + ph - v/ymax*ph
            p.append(f'<text x="{x0-6}" y="{yy+4}" text-anchor="end" font-family="{FONT}" font-size="9.5" fill="{MUTED}">{v}{"%" if key=="collusion" else ""}</text>')
        for rr in range(1, 6):
            xx = x0 + (rr-0.5)/5*pw
            p.append(f'<text x="{xx}" y="{y0+ph+16}" text-anchor="middle" font-family="{FONT}" font-size="10" fill="{MUTED}">{rr}</text>')
        for reg in regs:
            pts = []
            for rr in range(1, 6):
                b = by[(reg, rr)]
                val = b["collusion"]*100 if key == "collusion" else b["balance"]
                xx = x0 + (rr-0.5)/5*pw
                yy = y0 + ph - val/ymax*ph
                pts.append(f"{xx:.1f},{yy:.1f}")
            p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colors[reg]}" stroke-width="1.6"/>')
            for pt in pts:
                xx, yy = pt.split(",")
                p.append(f'<circle cx="{xx}" cy="{yy}" r="2.2" fill="{colors[reg]}"/>')
    for i, reg in enumerate(regs):
        lx = 60 + i*70
        p.append(f'<rect x="{lx}" y="{H-16}" width="10" height="7" fill="{colors[reg]}"/>')
        p.append(f'<text x="{lx+14}" y="{H-10}" font-family="{FONT}" font-size="10">{reg}</text>')
    p.append("</svg>")
    (FIG / "fig_econ_sandbox.svg").write_text("".join(p), encoding="utf-8")


def payments():
    W, H = 900, 430
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         '<defs><marker id="arr2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    p.append(box(30, 60, 150, 80, ["User budget", "(research funds)", "card top-up"], fs=11.5, bold=True))
    p.append(box(230, 60, 170, 80, ["Wallet / ledger", "double-entry", "idempotent"], fs=11.5, bold=True))
    p.append(box(450, 60, 150, 80, ["Agent runtime", "chooses offer"], fs=11.5, bold=True))
    p.append(box(650, 60, 200, 80, ["Merchant invoice", "real catalog price"], fs=11.5, bold=True))
    p.append(box(650, 220, 200, 80, ["Payment backend", "mock | Stripe test | live"], fs=11.5, bold=True))
    p.append(box(450, 220, 150, 80, ["Audit + stake", "penalty if hidden"], fs=11.5, bold=True))
    p.append(box(230, 220, 170, 80, ["Settlement", "charge id, receipt"], fs=11.5, bold=True))
    p.append(f'<path d="M180,100 L230,100" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arr2)"/>')
    p.append(f'<path d="M400,100 L450,100" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arr2)"/>')
    p.append(f'<path d="M600,100 L650,100" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arr2)"/>')
    p.append(f'<path d="M750,140 L750,220" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arr2)"/>')
    p.append(f'<path d="M650,260 L600,260" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr2)"/>')
    p.append(f'<path d="M450,260 L400,260" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arr2)"/>')
    p.append(f'<path d="M230,260 L200,260 L200,140" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arr2)"/>')
    p.append(f'<path d="M525,140 L525,220" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="4 3" marker-end="url(#arr2)"/>')
    p.append(f'<text x="452" y="345" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="{MUTED}">Solid: purchase flow. Dashed: sponsorship and audit feedback. Live mode is gated by an explicit flag and a spend cap.</text>')
    p.append("</svg>")
    (FIG / "fig_payments.svg").write_text("".join(p), encoding="utf-8")


if __name__ == "__main__":
    architecture()
    collusion()
    sandbox()
    econ()
    econ_sandbox()
    payments()
    print("figures written")
