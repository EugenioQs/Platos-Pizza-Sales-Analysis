"""
Generates the 3 background templates for the Plato's Pizza Power BI dashboard.
Outputs: visuals/template_p1_resumen.png
         visuals/template_p2_operaciones.png
         visuals/template_p3_menu.png

Usage: python visuals/generate_templates.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# ─── Configuración del canvas ────────────────────────────────────────────────
DPI = 96
W, H = 1280, 720

# ─── Paleta de colores ────────────────────────────────────────────────────────
BG          = "#252525"   # Gris oscuro — fondo general
PANEL       = "#181818"   # Más oscuro — panel header izquierdo
DECO_BG     = "#1E1E1E"   # Panel decorativo derecho
ACCENT      = "#E8901A"   # Naranja pizza — acentos y título
CARD        = "#FFFFFF"   # Cards blancas
CARD_BORDER = "#3A3A3A"   # Borde de cards (sutil)
WHITE       = "#FFFFFF"
DARK_TEXT   = "#1E1E1E"   # Texto en cards
LIGHT_TEXT  = "#CCCCCC"   # Texto secundario en dark bg
PILL_BG     = "#E8901A"   # Botón Filtros
SLICE_LINE  = "#C84B31"   # Líneas de la pizza

# ─── Layout compartido ────────────────────────────────────────────────────────
MARGIN      = 16
GAP         = 10
HEADER_H    = 88          # Altura del header
ROW1_Y      = HEADER_H + MARGIN
ROW1_H      = 68          # KPI cards


# ─── Helpers ─────────────────────────────────────────────────────────────────

def make_fig():
    """Crea figura en coordenadas de píxeles (0,0) = top-left."""
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)   # Y invertido: 0 = arriba
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    return fig, ax


def card(ax, x, y, w, h, title="", radius=10):
    """Card blanca con esquinas redondeadas y título opcional."""
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=CARD,
        edgecolor=CARD_BORDER,
        linewidth=0.8,
        zorder=2,
    )
    ax.add_patch(rect)
    if title:
        ax.text(
            x + 12, y + 14, title,
            fontsize=7.5, color="#555555",
            fontweight="bold", va="top", zorder=3,
            fontfamily="sans-serif",
        )


def draw_header(ax, subtitle):
    """Header común a todas las páginas."""
    # Panel izquierdo oscuro
    left = FancyBboxPatch(
        (0, 0), 360, HEADER_H,
        boxstyle="round,pad=0,rounding_size=0",
        facecolor=PANEL, zorder=1,
    )
    ax.add_patch(left)

    # Línea de acento debajo del panel izquierdo
    ax.plot([0, 360], [HEADER_H, HEADER_H], color=ACCENT, lw=2.5, zorder=3)

    # Texto de marca
    ax.text(20, 24, "PLATO'S PIZZA",
            color=ACCENT, fontsize=15, fontweight="bold",
            va="top", zorder=4, fontfamily="sans-serif")
    ax.text(20, 50, subtitle,
            color=LIGHT_TEXT, fontsize=9, va="top", zorder=4,
            fontfamily="sans-serif")
    ax.text(20, 68, "2015 Analysis · Plato's Pizza",
            color="#666666", fontsize=7, va="top", zorder=4,
            fontfamily="sans-serif")

    # Panel decorativo derecho con pizza
    deco = FancyBboxPatch(
        (900, 0), 380, HEADER_H,
        boxstyle="round,pad=0,rounding_size=0",
        facecolor=DECO_BG, zorder=1,
    )
    ax.add_patch(deco)
    ax.plot([900, 1280], [HEADER_H, HEADER_H], color=ACCENT, lw=2.5, zorder=3, alpha=0.5)

    draw_pizza(ax, cx=1185, cy=HEADER_H / 2, r=34)

    # Botón Filtros
    pill = FancyBboxPatch(
        (490, 28), 90, 28,
        boxstyle="round,pad=0,rounding_size=8",
        facecolor=PILL_BG, edgecolor="none", zorder=4,
    )
    ax.add_patch(pill)
    ax.text(535, 42, "Filters  ▼",
            color=WHITE, fontsize=8, fontweight="bold",
            ha="center", va="center", zorder=5,
            fontfamily="sans-serif")

    # Línea separadora header/contenido
    ax.plot([0, W], [HEADER_H, HEADER_H], color="#333333", lw=1, zorder=2)


def draw_pizza(ax, cx, cy, r):
    """Pizza decorativa simple."""
    # Crust
    ax.add_patch(plt.Circle((cx, cy), r, color="#D4A843", zorder=5))
    # Salsa
    ax.add_patch(plt.Circle((cx, cy), r * 0.86, color="#B03A2E", zorder=6))
    # Queso
    ax.add_patch(plt.Circle((cx, cy), r * 0.80, color="#F0C040", zorder=7))
    # Cortes de porción
    for angle in range(0, 360, 60):
        rad = np.radians(angle)
        ax.plot(
            [cx, cx + r * 0.80 * np.cos(rad)],
            [cy, cy + r * 0.80 * np.sin(rad)],
            color=SLICE_LINE, lw=1.2, zorder=8,
        )
    # Pepperoni
    for px, py in [(0.38, 0.18), (-0.28, 0.38), (0.08, -0.44), (-0.40, -0.18), (0.44, -0.22)]:
        ax.add_patch(plt.Circle((cx + px * r, cy + py * r), r * 0.10, color="#8B1A1A", zorder=9))
    # Mozzarella
    for mx, my in [(-0.18, 0.28), (0.28, -0.22), (-0.38, -0.05)]:
        ax.add_patch(plt.Circle((cx + mx * r, cy + my * r), r * 0.08, color="#FFF5E0", zorder=9))


def save(fig, filename):
    out = os.path.join(os.path.dirname(__file__), filename)
    fig.savefig(out, dpi=DPI, bbox_inches=None, pad_inches=0, facecolor=BG)
    plt.close(fig)
    print(f"  OK  {filename}")


# ─── PAGE 1 — Executive Summary ───────────────────────────────────────────────

def page1():
    fig, ax = make_fig()
    draw_header(ax, "Executive Summary")

    # Row 1 — 5 KPI cards
    kpi_titles = ["Total Revenue", "Total Orders", "Pizzas Sold", "Avg Ticket", "Orders / Day"]
    n = len(kpi_titles)
    kpi_w = (W - 2 * MARGIN - (n - 1) * GAP) / n
    for i, title in enumerate(kpi_titles):
        card(ax, MARGIN + i * (kpi_w + GAP), ROW1_Y, kpi_w, ROW1_H, title)

    # Row 2 — Line chart (60%) + Donut (40%)
    y2 = ROW1_Y + ROW1_H + GAP
    h2 = 222
    usable = W - 2 * MARGIN - GAP
    w2a = usable * 0.60
    w2b = usable * 0.40
    card(ax, MARGIN,            y2, w2a, h2, "Monthly Revenue Trend")
    card(ax, MARGIN + w2a + GAP, y2, w2b, h2, "Revenue by Category")

    # Row 3 — Bar chart (50%) + Operating context (50%)
    y3 = y2 + h2 + GAP
    h3 = H - MARGIN - y3
    w3 = (W - 2 * MARGIN - GAP) / 2
    card(ax, MARGIN,            y3, w3, h3, "Orders by Day of Week")
    card(ax, MARGIN + w3 + GAP, y3, w3, h3, "Operating Context")

    save(fig, "template_p1_resumen.png")


# ─── PAGE 2 — Operations ──────────────────────────────────────────────────────

def page2():
    fig, ax = make_fig()
    draw_header(ax, "Operations")

    # Row 1 — 3 KPI cards
    kpi_titles = ["Peak Hour", "Busiest Day", "Operating Days"]
    n = len(kpi_titles)
    kpi_w = (W - 2 * MARGIN - (n - 1) * GAP) / n
    for i, title in enumerate(kpi_titles):
        card(ax, MARGIN + i * (kpi_w + GAP), ROW1_Y, kpi_w, ROW1_H, title)

    # Row 2 — Heatmap left + Time Blocks right (expanded)
    y2 = ROW1_Y + ROW1_H + GAP
    usable = W - 2 * MARGIN - GAP
    w_heat = usable * 0.58
    w_right = usable * 0.42
    h2 = 240

    card(ax, MARGIN, y2, w_heat, h2, "Heat Map — Orders by Hour and Day")
    card(ax, MARGIN + w_heat + GAP, y2, w_right, h2, "Time Blocks")

    # Row 3 — Orders by Hour (40%) + Weekly Revenue (60%)
    y3 = y2 + h2 + GAP
    h3 = H - MARGIN - y3
    w3a = usable * 0.40
    w3b = usable * 0.60
    card(ax, MARGIN, y3, w3a, h3, "Orders Distribution by Hour")
    card(ax, MARGIN + w3a + GAP, y3, w3b, h3, "Revenue by Week of Year")

    save(fig, "template_p2_operaciones.png")


# ─── PAGE 3 — Menu & Products ─────────────────────────────────────────────────

def page3():
    fig, ax = make_fig()
    draw_header(ax, "Menu & Products")

    # Row 1 — 3 KPI cards
    kpi_titles = ["Pizzas on Menu", "Top Revenue Pizza", "Top Units Pizza"]
    n = len(kpi_titles)
    kpi_w = (W - 2 * MARGIN - (n - 1) * GAP) / n
    for i, title in enumerate(kpi_titles):
        card(ax, MARGIN + i * (kpi_w + GAP), ROW1_Y, kpi_w, ROW1_H, title)

    # Row 2 — Horizontal bar (55%) + Scatter (45%)
    y2 = ROW1_Y + ROW1_H + GAP
    h2 = 240
    usable = W - 2 * MARGIN - GAP
    w2a = usable * 0.55
    w2b = usable * 0.45
    card(ax, MARGIN,             y2, w2a, h2, "Revenue by Pizza — ABC Classification")
    card(ax, MARGIN + w2a + GAP, y2, w2b, h2, "Volume vs Revenue — Menu Outliers")

    # Row 3 — Stacked bar (50%) + Table (50%)
    y3 = y2 + h2 + GAP
    h3 = H - MARGIN - y3
    w3 = (W - 2 * MARGIN - GAP) / 2
    card(ax, MARGIN,             y3, w3, h3, "Most Popular Size by Category")
    card(ax, MARGIN + w3 + GAP,  y3, w3, h3, "Full Menu Performance")

    save(fig, "template_p3_menu.png")


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating templates...")
    page1()
    page2()
    page3()
    print("Done. Files in visuals/")
