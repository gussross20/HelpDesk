# -*- coding: utf-8 -*-
"""
Genera NET_FullStack_Lab_HelpDesk.pptx: 14 diapositivas del taller .NET Full Stack
avanzando estrictamente capa por capa: Domain -> Infrastructure -> Application -> Web.

Uso:
    python generar_presentacion.py

Instala python-pptx automáticamente si no está disponible.
"""

import importlib.util
import math
import subprocess
import sys
from pathlib import Path

if importlib.util.find_spec("pptx") is None:
    print("Instalando python-pptx...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

# --- Paleta Dark Tech ----------------------------------------------------------
BG = "0F172A"
CARD = "1E293B"
BORDER = "334155"
TEXT = "F8FAFC"
TEXT2 = "CBD5E1"
PURPLE = "7C3AED"
CYAN = "38BDF8"
RED = "EF4444"
GREEN = "10B981"
DARK_CODE = "0B1220"
PURPLE_DARK = "2E1A5E"
RED_DARK = "331C27"
GREEN_DARK = "12342C"
AMBER = "F59E0B"

FONT = "Segoe UI"
FONT_CODE = "Consolas"

SLIDE_W = 13.333
SLIDE_H = 7.5
M = 0.65
CONTENT_W = SLIDE_W - 2 * M
OUTPUT = "NET_FullStack_Lab_HelpDesk.pptx"

prs = Presentation()
prs.slide_width = Inches(SLIDE_W)
prs.slide_height = Inches(SLIDE_H)
BLANK = prs.slide_layouts[6]


def rgb(hex_color: str) -> RGBColor:
    return RGBColor.from_string(hex_color.lstrip("#"))


# --- Helpers de dibujo ---------------------------------------------------------
def no_line(shape):
    shape.line.fill.background()


def add_card(slide, x, y, w, h, fill=CARD, line=BORDER, line_width=1.0, rounded=True):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    if line is None:
        no_line(shape)
    else:
        shape.line.color.rgb = rgb(line)
        shape.line.width = Pt(line_width)
    if rounded:
        try:
            shape.adjustments[0] = 0.06
        except (IndexError, AttributeError):
            pass
    return shape


def _estimate_lines(text, width_in, size_pt, font=FONT):
    factor = 0.60 if font == FONT_CODE else 0.52
    chars_per_line = max(8, int(width_in * 72 / (size_pt * factor)))
    return sum(max(1, math.ceil(len(line) / chars_per_line)) for line in text.split("\n"))


def add_text(
    slide, x, y, w, h, text, size=16, color=TEXT, bold=False,
    font=FONT, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP,
    margin=0.04, line_spacing=1.12, min_size=None, fit=True,
):
    eff_size = float(size)
    min_size = float(min_size if min_size is not None else max(11, size - 3))
    if fit:
        while eff_size > min_size:
            usable_w = max(0.5, w - 2 * margin)
            lines = _estimate_lines(text, usable_w, eff_size, font)
            needed_h = lines * eff_size * 1.28 / 72 + 2 * margin
            if needed_h <= h:
                break
            eff_size -= 0.5

    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign

    for i, line in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(eff_size)
        run.font.bold = bold
        run.font.color.rgb = rgb(color)
    return box


def add_bullets(slide, x, y, w, h, items, size=16, gap=9, color=TEXT, bullet_color=CYAN):
    eff_size = float(size)
    min_size = max(12, size - 3)
    while eff_size > min_size:
        needed = sum(
            _estimate_lines(item, w - 0.45, eff_size, FONT) * eff_size * 1.25 / 72
            for item in items
        )
        needed += (len(items) - 1) * gap / 72 + 0.12
        if needed <= h:
            break
        eff_size -= 0.5

    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)

    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.14
        p.space_before = Pt(0)
        p.space_after = Pt(gap if i < len(items) - 1 else 0)

        rb = p.add_run()
        rb.text = "•  "
        rb.font.name = FONT
        rb.font.size = Pt(eff_size)
        rb.font.bold = True
        rb.font.color.rgb = rgb(bullet_color)

        rt = p.add_run()
        rt.text = item
        rt.font.name = FONT
        rt.font.size = Pt(eff_size)
        rt.font.color.rgb = rgb(color)
    return box


def add_arrow(slide, x1, y1, x2, y2, color=CYAN, width=2.0, head="end"):
    conn = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    )
    conn.line.color.rgb = rgb(color)
    conn.line.width = Pt(width)

    ln = conn._element.spPr.find(qn("a:ln"))
    if ln is None:
        ln = OxmlElement("a:ln")
        conn._element.spPr.append(ln)
    for tag in ("a:headEnd", "a:tailEnd"):
        old = ln.find(qn(tag))
        if old is not None:
            ln.remove(old)
    if head in ("start", "both"):
        he = OxmlElement("a:headEnd")
        he.set("type", "triangle")
        ln.append(he)
    if head in ("end", "both"):
        te = OxmlElement("a:tailEnd")
        te.set("type", "triangle")
        ln.append(te)
    return conn


def add_box_with_text(
    slide, x, y, w, h, text, fill=CARD, line=BORDER,
    text_color=TEXT, size=16, bold=False, font=FONT,
    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, rounded=True,
    line_width=1.0, margin=0.06,
):
    add_card(slide, x, y, w, h, fill=fill, line=line,
             line_width=line_width, rounded=rounded)
    return add_text(slide, x, y, w, h, text, size=size, color=text_color,
                    bold=bold, font=font, align=align, valign=valign,
                    margin=margin)


def add_base(title, page):
    slide = prs.slides.add_slide(BLANK)
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = rgb(BG)

    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(M), Inches(0.42), Inches(0.09), Inches(0.50)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = rgb(PURPLE)
    no_line(accent)

    add_text(slide, 0.90, 0.30, 11.55, 0.70, title, size=28, bold=True,
             color=TEXT, valign=MSO_ANCHOR.MIDDLE, min_size=24)

    sep = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(M), Inches(1.10), Inches(CONTENT_W), Inches(0.012)
    )
    sep.fill.solid()
    sep.fill.fore_color.rgb = rgb(BORDER)
    no_line(sep)

    add_text(slide, 12.10, 7.08, 0.55, 0.24, f"{page:02d}", size=9,
             color=TEXT2, align=PP_ALIGN.RIGHT, valign=MSO_ANCHOR.MIDDLE,
             fit=False)
    return slide


def add_step_badge(slide, cx, cy, number, color):
    badge = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(cx - 0.30), Inches(cy - 0.30), Inches(0.60), Inches(0.60)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = rgb(color)
    no_line(badge)
    add_text(slide, cx - 0.30, cy - 0.30, 0.60, 0.60, str(number),
             size=18, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, fit=False)


def add_dots(slide, x, y):
    for i, c in enumerate((RED, AMBER, GREEN)):
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(x + i * 0.22), Inches(y), Inches(0.11), Inches(0.11)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = rgb(c)
        no_line(dot)


# =============================================================================
# 1. PORTADA
# =============================================================================
slide = prs.slides.add_slide(BLANK)
bg = slide.background.fill
bg.solid()
bg.fore_color.rgb = rgb(BG)

for x, w, color in ((0.00, 0.16, PURPLE), (0.16, 0.05, CYAN)):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(x), Inches(0), Inches(w), Inches(SLIDE_H)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(color)
    no_line(bar)

add_card(slide, 0.95, 1.20, 11.45, 5.00, fill=CARD, line=BORDER, line_width=1.2)

add_text(slide, 1.25, 1.80, 10.85, 1.00, ".NET FULL STACK LAB",
         size=44, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=36)

add_text(slide, 1.25, 2.92, 10.85, 0.60, "De la idea al software profesional",
         size=22, color=CYAN, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=19)

rule = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(5.42), Inches(3.70), Inches(2.50), Inches(0.035)
)
rule.fill.solid()
rule.fill.fore_color.rgb = rgb(PURPLE)
no_line(rule)

add_text(slide, 1.25, 4.15, 10.85, 0.45,
         "C# · .NET · Blazor Server · SQL Server · Clean Architecture",
         size=16, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=14)

add_text(slide, 1.25, 4.70, 10.85, 0.45,
         "5° Semestre · 9:00 AM – 3:00 PM",
         size=16, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=14)

add_text(slide, 1.25, 5.55, 10.85, 0.35,
         "LABORATORIO · DOMAIN → INFRASTRUCTURE → APPLICATION → WEB",
         size=11, bold=True, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, fit=False)

# =============================================================================
# 2. EL PROBLEMA: ESPAGUETI VS. LIMPIA
# =============================================================================
slide = add_base("EL PROBLEMA: CÓDIGO ESPAGUETI VS. ARQUITECTURA LIMPIA", 2)

add_card(slide, 0.65, 1.42, 5.85, 5.25, fill=CARD, line=RED, line_width=1.6)
add_text(slide, 0.95, 1.70, 5.25, 0.50, "Código Espagueti", size=21, bold=True,
         color=RED, valign=MSO_ANCHOR.MIDDLE)
add_arrow(slide, 3.58, 2.35, 3.58, 2.70, color=RED, width=2.0)
add_box_with_text(
    slide, 0.95, 2.76, 5.25, 1.25,
    "Un botón de Blazor con\nHTML + Validaciones + SQL",
    fill=RED_DARK, line=RED, text_color=TEXT, size=16, margin=0.10,
)
add_arrow(slide, 3.58, 4.08, 3.58, 4.40, color=RED, width=2.0)
add_text(slide, 0.95, 4.48, 5.25, 1.45,
         "Funciona hoy, imposible de mantener mañana. Alta deuda técnica.",
         size=17, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.TOP, min_size=15)

add_card(slide, 6.83, 1.42, 5.85, 5.25, fill=CARD, line=GREEN, line_width=1.6)
add_text(slide, 7.13, 1.70, 5.25, 0.50, "Arquitectura Limpia", size=21, bold=True,
         color=GREEN, valign=MSO_ANCHOR.MIDDLE)

bw, gap, by, bh = 1.08, 0.30, 2.82, 0.95
bx = 7.14
labels = ["Web", "Application", "Domain", "Infrastructure"]
for i, label in enumerate(labels):
    add_box_with_text(slide, bx + i * (bw + gap), by, bw, bh, label,
                      fill=CARD, line=PURPLE if label == "Domain" else BORDER,
                      text_color=TEXT, size=12, bold=(label == "Domain"), margin=0.04)
for i in (0, 1):
    add_arrow(slide, bx + i * (bw + gap) + bw, by + bh / 2,
              bx + (i + 1) * (bw + gap), by + bh / 2, color=CYAN, width=1.8)
add_arrow(slide, bx + 3 * (bw + gap), by + bh / 2,
          bx + 2 * (bw + gap) + bw, by + bh / 2, color=PURPLE, width=2.2)
add_text(slide, bx + 2 * (bw + gap), 3.83, bw, 0.25, "NÚCLEO",
         size=10, bold=True, color=PURPLE, align=PP_ALIGN.CENTER, fit=False)

add_text(slide, 7.13, 4.48, 5.25, 1.45,
         "Cuatro capas con responsabilidades claras: bajo acoplamiento y mantenimiento sencillo.",
         size=17, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.TOP, min_size=15)

# =============================================================================
# 3. EL RETO DE HOY
# =============================================================================
slide = add_base("EL RETO DE HOY: SISTEMA HELPDESK", 3)

add_card(slide, 0.65, 1.42, 4.70, 5.25, fill=CARD, line=BORDER)
add_text(slide, 0.92, 1.68, 4.16, 0.48, "Sistema HelpDesk", size=20, bold=True,
         color=CYAN, valign=MSO_ANCHOR.MIDDLE)
add_bullets(
    slide, 0.92, 2.25, 4.16, 1.75,
    [
        "Mesa de ayuda para gestionar incidentes.",
        "3 tablas SQL Server: Categoria, Ticket y ComentarioTicket.",
        "Bitácora de comentarios por ticket.",
    ],
    size=15.5, gap=8,
)
add_text(slide, 0.92, 4.10, 4.16, 0.35, "Ciclo de vida del ticket", size=14,
         bold=True, color=TEXT2, valign=MSO_ANCHOR.MIDDLE, fit=False)

states = ["Abierto", "En Proceso", "Resuelto"]
sx, sw, sgap, sy, sh = 0.92, 1.18, 0.31, 4.55, 0.78
for i, st in enumerate(states):
    add_box_with_text(slide, sx + i * (sw + sgap), sy, sw, sh, st,
                      fill=CARD, line=BORDER, text_color=TEXT, size=12.5,
                      bold=True, margin=0.03)
for i in (0, 1):
    add_arrow(slide, sx + i * (sw + sgap) + sw, sy + sh / 2,
              sx + (i + 1) * (sw + sgap), sy + sh / 2, color=CYAN, width=1.8)
add_text(slide, 0.92, 5.55, 4.16, 0.45,
         "Estados modelados en EstadoTicket.cs", size=13, color=TEXT2,
         valign=MSO_ANCHOR.MIDDLE, fit=False)

fx, fy, fw, fh = 5.65, 1.42, 7.03, 5.25
add_card(slide, fx, fy, fw, fh, fill="111C31", line=BORDER, line_width=1.2)
bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(fx), Inches(fy),
                             Inches(fw), Inches(0.52))
bar.fill.solid()
bar.fill.fore_color.rgb = rgb(CARD)
no_line(bar)
add_dots(slide, fx + 0.22, fy + 0.20)
add_text(slide, fx + 1.05, fy + 0.06, fw - 1.30, 0.40,
         "helpdesk.local /tickets", size=12, color=TEXT2,
         valign=MSO_ANCHOR.MIDDLE, fit=False)
inner = add_card(slide, fx + 0.28, fy + 0.80, fw - 0.56, fh - 1.08,
                 fill=DARK_CODE, line=BORDER)
inner.line.dash_style = MSO_LINE_DASH_STYLE.DASH
add_text(slide, fx + 0.60, fy + 1.55, fw - 1.20, fh - 2.10,
         "[ ESPACIO RESERVADO:\nPegar aquí capturas de pantalla\nde HelpDesk corriendo ]",
         size=18, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, line_spacing=1.35, min_size=15)

# =============================================================================
# 4. MAPA DE LA ARQUITECTURA (ANALOGÍA DEL RESTAURANTE)
# =============================================================================
slide = add_base("MAPA DE LA ARQUITECTURA: ANALOGÍA DEL RESTAURANTE", 4)
add_text(slide, M, 1.35, CONTENT_W, 0.38,
         "Flujo de peticiones y dirección de las dependencias",
         size=14, color=TEXT2, valign=MSO_ANCHOR.MIDDLE, fit=False)

ax, ay, aw, ah, agap = 0.70, 1.95, 2.65, 2.05, 0.45
arch = [
    ("Web", "Mesero", "Recibe y muestra", CYAN),
    ("Application", "Chef", "Orquesta casos de uso", PURPLE),
    ("Domain", "Menú / Reglas", "Núcleo del negocio", PURPLE),
    ("Infrastructure", "Almacén / SQL", "Persistencia", CYAN),
]
for i, (name, role, desc, accent) in enumerate(arch):
    x = ax + i * (aw + agap)
    add_card(slide, x, ay, aw, ah, fill=CARD, line=accent,
             line_width=2.0 if i == 2 else 1.2)
    add_text(slide, x + 0.12, ay + 0.18, aw - 0.24, 0.45, name,
             size=16, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, min_size=14)
    add_text(slide, x + 0.12, ay + 0.70, aw - 0.24, 0.40, f"[ {role} ]",
             size=13, bold=True, color=accent, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, min_size=11.5)
    add_text(slide, x + 0.12, ay + 1.22, aw - 0.24, 0.55, desc,
             size=12.5, color=TEXT2, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.TOP, min_size=11)

for i in (0, 1):
    add_arrow(slide, ax + i * (aw + agap) + aw, ay + ah / 2,
              ax + (i + 1) * (aw + agap), ay + ah / 2, color=CYAN, width=2.2)
add_arrow(slide, ax + 3 * (aw + agap), ay + ah / 2,
          ax + 2 * (aw + agap) + aw, ay + ah / 2, color=PURPLE, width=2.6)

add_card(slide, 0.70, 4.75, 11.95, 1.25, fill=PURPLE_DARK, line=PURPLE, line_width=1.6)
add_text(slide, 1.00, 4.90, 11.35, 0.95,
         "Regla de Oro: las dependencias siempre apuntan hacia Domain. Domain es C# puro.",
         size=18, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=16)

# =============================================================================
# 5. CAPA 1 — TEORÍA
# =============================================================================
slide = add_base("CAPA 1 (DOMAIN): MODELADO ORIENTADO AL DOMINIO", 5)

theory = [
    ("1", "¿Qué es una Entidad?", PURPLE,
     "Objeto con identidad propia que representa un concepto del negocio.\n"
     "Ejemplo: Ticket, Categoria, ComentarioTicket."),
    ("2", "Llaves foráneas (FK)", CYAN,
     "CategoriaId y TicketId enlazan tablas y permiten reconstruir relaciones 1:N.\n"
     "Ejemplo: public int CategoriaId { get; set; }"),
    ("3", "Propiedades de navegación", GREEN,
     "Permiten recorrer el grafo en C#: Ticket.Categoria, Categoria.Tickets y Ticket.Comentarios."),
    ("4", "C# puro, sin dependencias", PURPLE,
     "Domain no referencia EF Core, SQL Server ni Blazor. Solo entidades, enums e interfaces.\n"
     "Así se mantiene estable ante cambios tecnológicos."),
]
tx, ty, tw, th, tgap = 0.65, 1.50, 5.85, 2.25, 0.33
for i, (num, title, color, body) in enumerate(theory):
    x = tx + (i % 2) * (tw + tgap)
    y = ty + (i // 2) * (th + 0.30)
    add_card(slide, x, y, tw, th, fill=CARD, line=BORDER)
    add_step_badge(slide, x + 0.42, y + 0.42, num, color)
    add_text(slide, x + 0.90, y + 0.18, tw - 1.15, 0.50, title,
             size=17, bold=True, color=TEXT, valign=MSO_ANCHOR.MIDDLE,
             min_size=15)
    add_text(slide, x + 0.28, y + 0.85, tw - 0.56, 1.20, body,
             size=14.5, color=TEXT2, valign=MSO_ANCHOR.TOP,
             line_spacing=1.18, min_size=12.5)

# =============================================================================
# 6. CAPA 1 — PRÁCTICA: DIAGRAMA ER
# =============================================================================
slide = add_base("CAPA 1 (DOMAIN): PRÁCTICA — DIAGRAMA ENTIDAD-RELACIÓN", 6)
add_text(slide, M, 1.32, CONTENT_W, 0.32,
         "Declare estas entidades en HelpDesk.Domain/Entities",
         size=14, color=TEXT2, valign=MSO_ANCHOR.MIDDLE, fit=False)

tables = [
    ("Categoria", ["Id (int PK)", "Nombre (string 100)", "Descripcion (string 250)"]),
    ("Ticket", [
        "Id (int PK)", "Titulo (string 150)", "Descripcion (string 1000)",
        "Prioridad (Enum)", "Estado (Enum)", "FechaCreacion (DateTime)",
        "CategoriaId (int FK)",
    ]),
    ("ComentarioTicket", [
        "Id (int PK)", "TicketId (int FK)", "Autor (string 100)",
        "Mensaje (string 500)", "Fecha (DateTime)",
    ]),
]
ex, ey, ew, eh, egap = 0.65, 1.78, 3.55, 4.35, 0.69
for i, (name, fields) in enumerate(tables):
    x = ex + i * (ew + egap)
    add_card(slide, x, ey, ew, eh, fill=CARD, line=CYAN, line_width=1.4)
    head = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(ey),
                                  Inches(ew), Inches(0.52))
    head.fill.solid()
    head.fill.fore_color.rgb = rgb(PURPLE if i == 1 else "26364F")
    no_line(head)
    add_text(slide, x + 0.10, ey, ew - 0.20, 0.52, name,
             size=15, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, fit=False)
    add_text(slide, x + 0.22, ey + 0.72, ew - 0.44, eh - 0.95,
             "\n".join(fields), size=13, color=TEXT2, font=FONT_CODE,
             valign=MSO_ANCHOR.TOP, line_spacing=1.30, min_size=11.5)

for i in (0, 1):
    x1 = ex + i * (ew + egap) + ew
    x2 = ex + (i + 1) * (ew + egap)
    add_arrow(slide, x1, ey + 2.15, x2, ey + 2.15, color=CYAN, width=2.4)
    add_text(slide, x1, ey + 1.72, x2 - x1, 0.34, "1:N",
             size=12, bold=True, color=CYAN, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, fit=False)

add_card(slide, 0.65, 6.35, 12.03, 0.55, fill=PURPLE_DARK, line=PURPLE)
add_text(slide, 0.95, 6.35, 11.43, 0.55,
         "Checkpoint Git: main ──▶ 01-domain", size=16, bold=True,
         color=CYAN, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE,
         min_size=14)

# =============================================================================
# 7. CAPA 2 — EF CORE Y REPOSITORY
# =============================================================================
slide = add_base("CAPA 2 (INFRASTRUCTURE): EF CORE CODE-FIRST Y REPOSITORY", 7)

top_cards = [
    ("HelpDeskDbContext", "Convierte entidades en tablas SQL Server mediante Fluent API y DbSet<T>."),
    ("Data Seeding", " Precarga 4 categorías con HasData() durante la creación del modelo."),
    ("Migraciones", "dotnet ef migrations add InitialCreate\ndotnet ef database update"),
]
tw3, tg3, ty3, th3 = 3.85, 0.24, 1.48, 1.65
for i, (title, body) in enumerate(top_cards):
    x = 0.65 + i * (tw3 + tg3)
    add_card(slide, x, ty3, tw3, th3, fill=CARD, line=BORDER)
    add_text(slide, x + 0.22, ty3 + 0.16, tw3 - 0.44, 0.40, title,
             size=16, bold=True, color=CYAN, valign=MSO_ANCHOR.MIDDLE,
             min_size=14)
    is_code = i == 2
    add_text(slide, x + 0.22, ty3 + 0.66, tw3 - 0.44, 0.82, body.strip(),
             size=13 if is_code else 14.5,
             color=TEXT if is_code else TEXT2,
             font=FONT_CODE if is_code else FONT,
             valign=MSO_ANCHOR.TOP, line_spacing=1.16, min_size=11.5)

add_card(slide, 0.65, 3.42, 5.85, 2.35, fill=CARD, line=BORDER)
add_text(slide, 0.92, 3.62, 5.31, 0.42, "Patrón Repository",
         size=17, bold=True, color=TEXT, valign=MSO_ANCHOR.MIDDLE)
add_box_with_text(slide, 0.92, 4.18, 2.35, 0.75, "ITicketRepository\n(contrato en Domain)",
                  fill=CARD, line=PURPLE, size=12.5, bold=True, margin=0.04)
add_arrow(slide, 3.27, 4.55, 3.75, 4.55, color=CYAN, width=2.0)
add_box_with_text(slide, 3.75, 4.18, 2.45, 0.75, "TicketRepository\n(SQL Server)",
                  fill=CARD, line=CYAN, size=12.5, bold=True, margin=0.04)
add_text(slide, 0.92, 5.10, 5.31, 0.48,
         "Desacopla consultas de la lógica de negocio.",
         size=14.5, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=13)

add_card(slide, 6.83, 3.42, 5.85, 2.35, fill=CARD, line=BORDER)
add_text(slide, 7.10, 3.62, 5.31, 0.42, "Eager Loading con .Include()",
         size=17, bold=True, color=TEXT, valign=MSO_ANCHOR.MIDDLE,
         min_size=15)
add_card(slide, 7.10, 4.18, 5.31, 0.80, fill=DARK_CODE, line=CYAN)
add_text(slide, 7.10, 4.18, 5.31, 0.80,
         ".Include(t => t.Categoria)\n.Include(t => t.Comentarios)",
         size=13, color=CYAN, font=FONT_CODE, valign=MSO_ANCHOR.MIDDLE,
         margin=0.06, min_size=12)
add_text(slide, 7.10, 5.10, 5.31, 0.48,
         "Evita referencias nulas y consultas N+1.",
         size=14.5, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=13)

add_card(slide, 0.65, 6.05, 12.03, 0.55, fill=PURPLE_DARK, line=PURPLE)
add_text(slide, 0.95, 6.05, 11.43, 0.55,
         "Checkpoint Git: 01-domain ──▶ 02-infrastructure",
         size=16, bold=True, color=CYAN, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=14)

# =============================================================================
# 8. CAPA 3 — DTOs Y VALIDACIONES
# =============================================================================
slide = add_base("CAPA 3 (APPLICATION): DTOs Y VALIDACIONES", 8)

dx, dy, dw, dh, dgap = 0.62, 1.60, 2.70, 1.25, 0.45
steps = ["[ Formulario Blazor ]", "[ CrearTicketDto ]", "[ TicketService ]", "[ Entidad Ticket ]"]
for i, st in enumerate(steps):
    add_box_with_text(slide, dx + i * (dw + dgap), dy, dw, dh, st,
                      fill=CARD, line=PURPLE if i == 1 else BORDER,
                      text_color=TEXT, size=15, bold=True, margin=0.06)
for i in (0, 1, 2):
    add_arrow(slide, dx + i * (dw + dgap) + dw, dy + dh / 2,
              dx + (i + 1) * (dw + dgap), dy + dh / 2, color=CYAN, width=2.2)

add_card(slide, 0.65, 3.35, 5.85, 2.35, fill=RED_DARK, line=RED)
add_text(slide, 0.92, 3.58, 5.31, 0.42, "Anti-patrón: Overposting",
         size=17, bold=True, color=RED, valign=MSO_ANCHOR.MIDDLE,
         min_size=15)
add_text(slide, 0.92, 4.15, 5.31, 1.25,
         "Enlazar el formulario directamente a la entidad Ticket permite modificar Id, "
         "FechaCreacion o Estado desde HTTP.",
         size=15.5, color=TEXT2, valign=MSO_ANCHOR.TOP,
         line_spacing=1.18, min_size=13.5)

add_card(slide, 6.83, 3.35, 5.85, 2.35, fill=GREEN_DARK, line=GREEN)
add_text(slide, 7.10, 3.58, 5.31, 0.42, "Buena práctica: DataAnnotations",
         size=17, bold=True, color=GREEN, valign=MSO_ANCHOR.MIDDLE,
         min_size=15)
add_card(slide, 7.10, 4.15, 5.31, 0.95, fill=DARK_CODE, line=GREEN)
add_text(slide, 7.10, 4.15, 5.31, 0.95,
         "[Required]   [StringLength]   [Range]",
         size=13, color=GREEN, font=FONT_CODE, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, margin=0.05, min_size=12)
add_text(slide, 7.10, 5.22, 5.31, 0.35,
         "El DTO expone solo los campos permitidos.",
         size=14, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=12.5)

add_text(slide, 0.65, 6.05, 12.03, 0.45,
         "Application no conoce EF Core: solo interactúa con contratos de Domain.",
         size=14, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=12.5)

# =============================================================================
# 9. CAPA 3 — RESULT PATTERN
# =============================================================================
slide = add_base("CAPA 3 (APPLICATION): EL RESULT PATTERN", 9)

add_card(slide, 0.65, 1.48, 5.85, 2.85, fill=CARD, line=RED, line_width=1.6)
add_text(slide, 0.95, 1.70, 5.25, 0.45, "EVITAR", size=16, bold=True,
         color=RED, valign=MSO_ANCHOR.MIDDLE, fit=False)
add_card(slide, 0.95, 2.28, 5.25, 1.05, fill=DARK_CODE, line=RED)
add_text(slide, 0.95, 2.28, 5.25, 1.05,
         'throw new Exception("Ticket cerrado");',
         size=14, color=RED, font=FONT_CODE, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, margin=0.05, min_size=13)
add_text(slide, 0.95, 3.52, 5.25, 0.60,
         "Rompe el flujo y abusa de try/catch.",
         size=15.5, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=14)

add_card(slide, 6.83, 1.48, 5.85, 2.85, fill=CARD, line=GREEN, line_width=1.6)
add_text(slide, 7.13, 1.70, 5.25, 0.45, "USAR", size=16, bold=True,
         color=GREEN, valign=MSO_ANCHOR.MIDDLE, fit=False)
add_card(slide, 7.13, 2.28, 5.25, 1.05, fill=DARK_CODE, line=GREEN)
add_text(slide, 7.13, 2.28, 5.25, 1.05,
         'return Result.Failure("Ticket cerrado");',
         size=14, color=GREEN, font=FONT_CODE, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, margin=0.05, min_size=13)
add_text(slide, 7.13, 3.52, 5.25, 0.60,
         "Control explícito de reglas de negocio.",
         size=15.5, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=14)

add_card(slide, 0.65, 4.62, 12.03, 1.18, fill=CARD, line=BORDER)
add_text(slide, 0.95, 4.78, 11.43, 0.40, "Reglas de negocio en TicketService",
         size=16, bold=True, color=CYAN, valign=MSO_ANCHOR.MIDDLE)
add_text(slide, 0.95, 5.18, 11.43, 0.45,
         "Un ticket Resuelto no admite nuevos comentarios ni reversión a estados anteriores: se devuelve Result.Failure.",
         size=14.5, color=TEXT2, valign=MSO_ANCHOR.MIDDLE, min_size=13)

add_card(slide, 0.65, 6.05, 12.03, 0.55, fill=PURPLE_DARK, line=PURPLE)
add_text(slide, 0.95, 6.05, 11.43, 0.55,
         "Checkpoint Git: 02-infrastructure ──▶ 03-application",
         size=16, bold=True, color=CYAN, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=14)

# =============================================================================
# 10. CAPA 4 — INYECCIÓN DE DEPENDENCIAS
# =============================================================================
slide = add_base("CAPA 4 (WEB): INYECCIÓN DE DEPENDENCIAS (SOLID - D)", 10)

add_card(slide, 1.00, 1.45, 11.33, 2.25, fill=DARK_CODE, line=PURPLE, line_width=1.6)
add_text(slide, 1.30, 1.68, 10.73, 1.80,
         "// DependencyInjection.cs (Infrastructure)\n"
         "services.AddScoped<ITicketRepository, TicketRepository>();\n"
         "// Program.cs (Web)\n"
         "builder.Services.AddScoped<ITicketService, TicketService>();",
         size=13.5, color=TEXT, font=FONT_CODE, valign=MSO_ANCHOR.MIDDLE,
         line_spacing=1.30, margin=0.06, min_size=12)

add_card(slide, 0.65, 4.05, 5.85, 2.20, fill=CARD, line=BORDER)
add_text(slide, 0.95, 4.28, 5.25, 0.45, "Inversión de Dependencias",
         size=18, bold=True, color=CYAN, valign=MSO_ANCHOR.MIDDLE,
         min_size=16)
add_text(slide, 0.95, 4.90, 5.25, 1.05,
         "Program.cs conecta interfaces con implementaciones concretas; la UI depende de abstracciones.",
         size=15.5, color=TEXT2, valign=MSO_ANCHOR.TOP,
         line_spacing=1.18, min_size=13.5)

add_card(slide, 6.83, 4.05, 5.85, 2.20, fill=CARD, line=BORDER)
add_text(slide, 7.13, 4.28, 5.25, 0.45, "Ciclo de vida Scoped",
         size=18, bold=True, color=CYAN, valign=MSO_ANCHOR.MIDDLE,
         min_size=16)
add_text(slide, 7.13, 4.90, 5.25, 1.05,
         "Una instancia limpia por sesión de usuario en Blazor Server; se libera al terminar el circuito.",
         size=15.5, color=TEXT2, valign=MSO_ANCHOR.TOP,
         line_spacing=1.18, min_size=13.5)

add_text(slide, 0.65, 6.45, 12.03, 0.35,
         " database.Migrate() se ejecuta en desarrollo para aplicar InitialCreate automáticamente.",
         size=13, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=12)

# =============================================================================
# 11. CAPA 4 — BLAZOR SERVER REACTIVO
# =============================================================================
slide = add_base("CAPA 4 (WEB): BLAZOR SERVER REACTIVO", 11)

cards = [
    ('@page "/tickets"', "Rutas", "Define el enrutamiento URL del componente.", PURPLE),
    ("@inject ITicketService", "Desacoplamiento", "Conecta la vista con el servicio sin tocar SQL Server.", CYAN),
    ("EditForm + @bind", "Formularios", "Formularios reactivos en C# puro vía SignalR (sin JavaScript).", GREEN),
]
cx, cw, cgap, cy, ch = 0.65, 3.85, 0.24, 1.45, 4.40
for i, (code, label, desc, color) in enumerate(cards):
    x = cx + i * (cw + cgap)
    add_card(slide, x, cy, cw, ch, fill=CARD, line=BORDER)
    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(cy),
                                    Inches(cw), Inches(0.07))
    accent.fill.solid()
    accent.fill.fore_color.rgb = rgb(color)
    no_line(accent)
    add_text(slide, x + 0.25, cy + 0.28, cw - 0.50, 0.32, label.upper(),
             size=11, bold=True, color=color, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, fit=False)
    add_card(slide, x + 0.25, cy + 0.72, cw - 0.50, 0.90,
             fill=DARK_CODE, line=BORDER)
    add_text(slide, x + 0.25, cy + 0.72, cw - 0.50, 0.90, code,
             size=14, color=TEXT, font=FONT_CODE, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, margin=0.04, min_size=13)
    add_text(slide, x + 0.25, cy + 1.85, cw - 0.50, 2.30, desc,
             size=16, color=TEXT2, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.TOP, min_size=14, line_spacing=1.20)

add_card(slide, 0.65, 6.10, 12.03, 0.60, fill=CARD, line=BORDER)
add_text(slide, 0.95, 6.10, 11.43, 0.60,
         "Checkpoint Git: 03-application ──▶ 04-web-tablero",
         size=16, bold=True, color=CYAN, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=14)

# =============================================================================
# 12. PRUEBAS FUNCIONALES Y DESPLIEGUE
# =============================================================================
slide = add_base("PRUEBAS FUNCIONALES Y DESPLIEGUE", 12)

flow = ["UI (Blazor)", "TicketService", "TicketRepository", "SQL Server"]
fx0, fy0, fw0, fh0, fgap0 = 0.70, 1.65, 2.65, 1.55, 0.45
for i, label in enumerate(flow):
    add_box_with_text(slide, fx0 + i * (fw0 + fgap0), fy0, fw0, fh0, label,
                      fill=CARD, line=PURPLE if i in (1, 2) else BORDER,
                      text_color=TEXT, size=15, bold=True, margin=0.06)
for i in (0, 1, 2):
    add_arrow(slide, fx0 + i * (fw0 + fgap0) + fw0, fy0 + fh0 / 2,
              fx0 + (i + 1) * (fw0 + fgap0), fy0 + fh0 / 2,
              color=CYAN, width=2.2)

add_card(slide, 0.65, 3.60, 5.85, 2.55, fill=CARD, line=BORDER)
add_text(slide, 0.95, 3.85, 5.31, 0.45, "Validación End-to-End",
         size=18, bold=True, color=CYAN, valign=MSO_ANCHOR.MIDDLE,
         min_size=16)
add_bullets(slide, 0.95, 4.45, 5.31, 1.45,
            ["Alta de ticket desde el formulario.",
             "Filtros y bitácora en el tablero.",
             "Reglas de negocio aplicadas desde Application."],
            size=14.5, gap=8)

add_card(slide, 6.83, 3.60, 5.85, 2.55, fill=CARD, line=BORDER)
add_text(slide, 7.13, 3.85, 5.31, 0.45, "Empaquetado y Producción",
         size=18, bold=True, color=CYAN, valign=MSO_ANCHOR.MIDDLE,
         min_size=16)
add_card(slide, 7.13, 4.45, 5.31, 0.70, fill=DARK_CODE, line=GREEN)
add_text(slide, 7.13, 4.45, 5.31, 0.70, "dotnet publish -c Release",
         size=13.5, color=GREEN, font=FONT_CODE, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, margin=0.05, min_size=12.5)
add_text(slide, 7.13, 5.30, 5.31, 0.60,
         "Binarios listos para IIS, Linux o Azure.",
         size=15, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=13.5)

# =============================================================================
# 13. EL RETO FINAL
# =============================================================================
slide = add_base("EL RETO FINAL (ÚLTIMOS 50 MINUTOS)", 13)

add_card(slide, M, 1.38, CONTENT_W, 0.78, fill=PURPLE_DARK, line=PURPLE, line_width=1.6)
add_text(slide, 0.95, 1.38, CONTENT_W - 0.60, 0.78,
         "Punto de partida: git checkout 04-web-tablero",
         size=18, bold=True, color=CYAN, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=16)

levels = [
    ("Nivel 1 (Obligatorio)", PURPLE,
     "Vista /tickets/{Id:int} con cambio de estado, bitácora de comentarios y bloqueo cuando el ticket esté Resuelto."),
    ("Nivel 2 (Extra)", CYAN,
     "Buscador por título en el tablero pasando el filtro hasta TicketRepository."),
    ("Nivel 3 (Extra)", GREEN,
     "Permitir eliminar tickets únicamente en estado Abierto."),
]
lx, lw, lgap, ly, lh = 0.65, 3.85, 0.24, 2.42, 3.25
for i, (title, color, desc) in enumerate(levels):
    x = lx + i * (lw + lgap)
    add_card(slide, x, ly, lw, lh, fill=CARD, line=BORDER)
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(ly),
                                    Inches(lw), Inches(0.66))
    header.fill.solid()
    header.fill.fore_color.rgb = rgb(color)
    no_line(header)
    add_text(slide, x + 0.15, ly, lw - 0.30, 0.66, title,
             size=16, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.MIDDLE, fit=False)
    add_text(slide, x + 0.28, ly + 0.88, lw - 0.56, 2.15, desc,
             size=15.5, color=TEXT2, align=PP_ALIGN.CENTER,
             valign=MSO_ANCHOR.TOP, min_size=13.5, line_spacing=1.22)

add_text(slide, 0.65, 5.92, 12.03, 0.40,
         "Revisión final comparando arquitectura contra la rama `final`.",
         size=14, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, min_size=12.5)

# =============================================================================
# 14. CIERRE Y SIGUIENTES PASOS
# =============================================================================
slide = add_base("CIERRE Y SIGUIENTES PASOS", 14)

add_card(slide, 0.65, 1.48, 3.85, 4.95, fill=CARD, line=PURPLE, line_width=1.4)
add_text(slide, 0.92, 1.75, 3.31, 0.45, "Comparación contra final",
         size=17, bold=True, color=PURPLE, valign=MSO_ANCHOR.MIDDLE,
         min_size=15)
add_card(slide, 0.92, 2.35, 3.31, 0.80, fill=DARK_CODE, line=CYAN)
add_text(slide, 0.92, 2.35, 3.31, 0.80,
         "git diff 04-web-tablero..final",
         size=12.5, color=CYAN, font=FONT_CODE, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, margin=0.04, min_size=11.5)
add_text(slide, 0.92, 3.35, 3.31, 2.70,
         "Revisa qué faltó en DetalleTicket.razor y confirma que las reglas de negocio vivan en Application, no en la UI.",
         size=15, color=TEXT2, valign=MSO_ANCHOR.TOP,
         line_spacing=1.20, min_size=13)

add_card(slide, 4.74, 1.48, 3.85, 4.95, fill=CARD, line=BORDER)
add_text(slide, 5.01, 1.75, 3.31, 0.45, "Lo aprendido",
         size=17, bold=True, color=CYAN, valign=MSO_ANCHOR.MIDDLE,
         min_size=15)
add_bullets(slide, 5.01, 2.40, 3.31, 3.70,
            ["Domain: entidades y reglas puras.",
             "Infrastructure: EF Core, repositorios y migraciones.",
             "Application: DTOs, Result y servicios.",
             "Web: DI, Blazor Server y SignalR.",
             "Checkpoints Git por capa."],
            size=14.5, gap=11, bullet_color=GREEN)

add_card(slide, 8.83, 1.48, 3.85, 4.95, fill=CARD, line=GREEN, line_width=1.4)
add_text(slide, 9.10, 1.75, 3.31, 0.45, "Siguientes pasos",
         size=17, bold=True, color=GREEN, valign=MSO_ANCHOR.MIDDLE,
         min_size=15)
add_text(slide, 9.10, 2.45, 3.31, 1.30,
         "Pruebas unitarias del TicketService con mocks de repositorio y CI/CD.",
         size=15, color=TEXT2, valign=MSO_ANCHOR.TOP,
         line_spacing=1.20, min_size=13)
add_card(slide, 9.10, 4.00, 3.31, 1.55, fill=GREEN_DARK, line=GREEN)
add_text(slide, 9.10, 4.00, 3.31, 1.55,
         "ESPACIO PARA\nPREGUNTAS",
         size=18, bold=True, color=TEXT, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, line_spacing=1.25, min_size=16)

add_text(slide, 0.65, 6.65, 12.03, 0.35,
         ".NET Full Stack Lab · Gracias",
         size=13, color=TEXT2, align=PP_ALIGN.CENTER,
         valign=MSO_ANCHOR.MIDDLE, fit=False)

# --- Guardado y verificación --------------------------------------------------
out_path = Path(__file__).resolve().parent / OUTPUT
prs.save(out_path)

assert len(prs.slides) == 14, f"Se esperaban 14 diapositivas, hay {len(prs.slides)}"
assert out_path.exists() and out_path.stat().st_size > 0, "El archivo no se generó"

bounds_issues = []
for idx, s in enumerate(prs.slides, 1):
    for sh in s.shapes:
        if (sh.left < 0 or sh.top < 0 or
                sh.left + sh.width > prs.slide_width or
                sh.top + sh.height > prs.slide_height):
            bounds_issues.append((idx, sh.shape_type))

print(f"OK: {out_path.name} creado sin errores ({out_path.stat().st_size:,} bytes).")
print(f"Diapositivas: {len(prs.slides)} | Formato: 16:9 ({SLIDE_W} x {SLIDE_H} in)")
print(f"Formas fuera del lienzo: {len(bounds_issues)}")
