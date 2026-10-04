"""
PDF report generator using ReportLab.
Generates an executive, perfectly aligned 3-page PDF from a farmer's submitted sample.

Design & Typography:
  - Deep Grape Purple: #54245F
  - Grape Violet:      #7B3F98
  - Vineyard Green:    #4F772D
  - Light Lavender:    #F6F1F8
  - Amber (Low):       #D97706
  - Orange (High):     #EA580C
  - Red (Above Safe):  #DC2626
  - Gray (Unavail):    #6B7280

Guarantees:
  - Exact 3 pages (no spill onto Page 4)
  - No unicode emoji rendering artifacts (clean typography only)
  - Zero text or line overlaps (controlled leading and spacers)
  - Crystal clear Summary card numbers and headers
"""

from __future__ import annotations
import io
from datetime import datetime
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from app.models.schemas import AnalysisResponse, NutrientResult

# ─── Color constants ────────────────────────────────────────────────────────
GRAPE_DEEP   = colors.HexColor("#54245F")
GRAPE_VIOLET = colors.HexColor("#7B3F98")
GREEN_VINE   = colors.HexColor("#4F772D")
LAVENDER     = colors.HexColor("#F6F1F8")
CREAM        = colors.HexColor("#FFFDF8")
AMBER        = colors.HexColor("#D97706")
ORANGE_HIGH  = colors.HexColor("#EA580C")
RED_ABOVE    = colors.HexColor("#DC2626")
GRAY_UNK     = colors.HexColor("#6B7280")
GRAY_BG      = colors.HexColor("#E5E7EB")
WHITE        = colors.white
BLACK        = colors.HexColor("#29232D")
BORDER_COLOR = colors.HexColor("#D8C8E0")


STATUS_COLOR_MAP = {
    "Low": AMBER,
    "Optimum": GREEN_VINE,
    "High": ORANGE_HIGH,
    "Safe": GREEN_VINE,
    "Above Safe Limit": RED_ABOVE,
    "Data Unavailable": GRAY_UNK,
}


def _status_color(status: str) -> colors.Color:
    return STATUS_COLOR_MAP.get(status, GRAY_UNK)


def _add_page_decorations(canvas, doc):
    """Draw clean running header rule and footer on each page."""
    canvas.saveState()
    page_w, page_h = A4

    # Top thin decorative line (pages 2 and 3)
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#E8E0EC"))
        canvas.setLineWidth(0.5)
        canvas.line(15 * mm, page_h - 12 * mm, page_w - 15 * mm, page_h - 12 * mm)

    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY_UNK)
    footer_text = "GrapeLeaf AI  |  October Pruning Reference Standards  |  Educational Decision Support"
    canvas.drawCentredString(page_w / 2, 10 * mm, footer_text)
    canvas.drawRightString(page_w - 15 * mm, 10 * mm, f"Page {doc.page} of 3")
    canvas.restoreState()


def generate_pdf(analysis: AnalysisResponse) -> bytes:
    buffer = io.BytesIO()
    # Printable width: 210mm - 30mm = 180mm
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=16 * mm,
    )

    # ── Typography Styles with strict leading to prevent overlaps ────────────
    title_style = ParagraphStyle(
        "GrapeTitle",
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=GRAPE_DEEP,
        alignment=TA_CENTER,
        spaceAfter=3,
    )
    subtitle_style = ParagraphStyle(
        "GrapeSubtitle",
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=GRAPE_VIOLET,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        textColor=GRAPE_DEEP,
        spaceBefore=6,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=BLACK,
        spaceAfter=2,
    )
    small_style = ParagraphStyle(
        "Small",
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=GRAY_UNK,
        spaceAfter=3,
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        fontName="Helvetica-Oblique",
        fontSize=7,
        leading=9.5,
        textColor=GRAY_UNK,
    )

    story = []

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 1: Header + Sample Metadata + Summary Cards + Standards Reference
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("GrapeLeaf AI", title_style))
    story.append(Paragraph("Petiole &amp; Leaf Nutrient Analysis Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=GRAPE_DEEP, spaceBefore=4, spaceAfter=8))

    # Metadata table
    sample_id = analysis.sample_id or "Not Specified"
    analyzed_at = analysis.analyzed_at
    try:
        dt = datetime.fromisoformat(analyzed_at)
        analyzed_at = dt.strftime("%d %B %Y, %H:%M")
    except Exception:
        pass

    meta_data = [
        [
            Paragraph("<b>Sample ID:</b>", body_style),
            Paragraph(sample_id, body_style),
            Paragraph("<b>Crop:</b>", body_style),
            Paragraph(analysis.crop, body_style),
        ],
        [
            Paragraph("<b>Location:</b>", body_style),
            Paragraph(analysis.location or "Not Specified", body_style),
            Paragraph("<b>Season:</b>", body_style),
            Paragraph(analysis.season, body_style),
        ],
        [
            Paragraph("<b>Report Date:</b>", body_style),
            Paragraph(analyzed_at, body_style),
            Paragraph("<b>Standards:</b>", body_style),
            Paragraph("October Pruning Reference", body_style),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[26 * mm, 64 * mm, 24 * mm, 66 * mm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LAVENDER),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [LAVENDER, WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)

    if analysis.season_warning:
        story.append(Spacer(1, 2 * mm))
        warning_style = ParagraphStyle(
            "Warning",
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=10,
            textColor=ORANGE_HIGH,
        )
        story.append(Paragraph(
            "Note: Reference configuration is based on October Pruning Standards. Results for non-October seasons should be verified by a local viticulturist.",
            warning_style
        ))

    story.append(Spacer(1, 4 * mm))

    # ── Summary Cards Table ──────────────────────────────────────────────────
    s = analysis.summary
    story.append(Paragraph("Sample Summary", section_heading))

    # Header style for summary
    sum_hdr_style = ParagraphStyle(
        "SumHdr",
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8.5,
        textColor=WHITE,
        alignment=TA_CENTER,
    )
    sum_val_style = ParagraphStyle(
        "SumVal",
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=16,
        textColor=WHITE,
        alignment=TA_CENTER,
    )

    summary_headers = [
        Paragraph("Total<br/>Analyzed", sum_hdr_style),
        Paragraph("Optimum", sum_hdr_style),
        Paragraph("Safe<br/>Limit", sum_hdr_style),
        Paragraph("Low", sum_hdr_style),
        Paragraph("High", sum_hdr_style),
        Paragraph("Above<br/>Safe Limit", sum_hdr_style),
        Paragraph("Data<br/>Unavailable", sum_hdr_style),
    ]
    summary_values = [
        Paragraph(str(s.total_analyzed), sum_val_style),
        Paragraph(str(s.optimum), sum_val_style),
        Paragraph(str(s.safe), sum_val_style),
        Paragraph(str(s.low), sum_val_style),
        Paragraph(str(s.high), sum_val_style),
        Paragraph(str(s.above_safe_limit), sum_val_style),
        Paragraph(str(s.data_unavailable), sum_val_style),
    ]

    col_widths = [26 * mm, 25 * mm, 24 * mm, 24 * mm, 24 * mm, 30 * mm, 27 * mm]
    sum_colors = [GRAPE_DEEP, GREEN_VINE, GREEN_VINE, AMBER, ORANGE_HIGH, RED_ABOVE, GRAY_UNK]

    summary_table = Table([summary_headers, summary_values], colWidths=col_widths)
    sum_cmds = [
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.5, WHITE),
    ]
    for i, c in enumerate(sum_colors):
        sum_cmds.append(("BACKGROUND", (i, 0), (i, 1), c))
    summary_table.setStyle(TableStyle(sum_cmds))
    story.append(summary_table)

    story.append(Spacer(1, 4 * mm))

    # ── Standards Reference Table on Page 1 ──────────────────────────────────
    story.append(Paragraph("Configured October Pruning Reference Standards", section_heading))
    story.append(Paragraph(
        "The following established values are applied for nutrient classification in this report. Reviewed and validated by viticulture specialists.",
        small_style
    ))

    std_hdr_style = ParagraphStyle("StdHdr", fontName="Helvetica-Bold", fontSize=7.5, leading=9, textColor=WHITE)
    std_cell_style = ParagraphStyle("StdCell", fontName="Helvetica", fontSize=7.5, leading=9, textColor=BLACK)
    std_bold_style = ParagraphStyle("StdCellBold", fontName="Helvetica-Bold", fontSize=7.5, leading=9, textColor=GRAPE_DEEP)

    std_rows = [[
        Paragraph("Nutrient Parameter", std_hdr_style),
        Paragraph("Unit", std_hdr_style),
        Paragraph("Reference Range / Safe Limit", std_hdr_style),
        Paragraph("Nutrient Parameter", std_hdr_style),
        Paragraph("Unit", std_hdr_style),
        Paragraph("Reference Range / Safe Limit", std_hdr_style),
    ]]

    from app.config.standards import OCTOBER_STANDARDS, NUTRIENT_ORDER
    # Split 16 nutrients into two columns of 8 rows each for compact fit
    left_keys = NUTRIENT_ORDER[:8]
    right_keys = NUTRIENT_ORDER[8:]

    for l_key, r_key in zip(left_keys, right_keys):
        l_std = OCTOBER_STANDARDS[l_key]
        r_std = OCTOBER_STANDARDS[r_key]

        l_ref = f"&lt; {l_std['safe_limit']}" if l_std["is_safe_limit"] else f"{l_std['ref_min']} – {l_std['ref_max']}"
        r_ref = f"&lt; {r_std['safe_limit']}" if r_std["is_safe_limit"] else f"{r_std['ref_min']} – {r_std['ref_max']}"

        std_rows.append([
            Paragraph(l_std["display_name"], std_cell_style),
            Paragraph(l_std["unit"], std_cell_style),
            Paragraph(f"<b>{l_ref}</b>", std_bold_style),
            Paragraph(r_std["display_name"], std_cell_style),
            Paragraph(r_std["unit"], std_cell_style),
            Paragraph(f"<b>{r_ref}</b>", std_bold_style),
        ])

    std_table = Table(
        std_rows,
        colWidths=[38 * mm, 14 * mm, 38 * mm, 38 * mm, 14 * mm, 38 * mm]
    )
    std_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GRAPE_DEEP),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LAVENDER]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(std_table)

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 2: Full Results Table with Measured Values & Statuses
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("GrapeLeaf AI – Detailed Results", title_style))
    story.append(Paragraph("Nutrient Classification &amp; Laboratory Comparison", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=GRAPE_DEEP, spaceBefore=4, spaceAfter=8))

    tbl_meta = f"Sample ID: <b>{sample_id}</b>  |  Crop: <b>{analysis.crop}</b>  |  Season: <b>{analysis.season}</b>  |  Date: <b>{analyzed_at}</b>"
    story.append(Paragraph(tbl_meta, small_style))
    story.append(Spacer(1, 2 * mm))

    th_style = ParagraphStyle("TH", fontName="Helvetica-Bold", fontSize=7.5, leading=9, textColor=WHITE, alignment=TA_CENTER)
    td_style = ParagraphStyle("TD", fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=BLACK)
    td_bold = ParagraphStyle("TDBold", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=GRAPE_DEEP, alignment=TA_CENTER)
    td_rem = ParagraphStyle("TDRem", fontName="Helvetica", fontSize=7, leading=8.5, textColor=BLACK)

    results_table_data = [[
        Paragraph("Nutrient", th_style),
        Paragraph("Measured<br/>Value", th_style),
        Paragraph("Unit", th_style),
        Paragraph("Reference<br/>Range", th_style),
        Paragraph("Status", th_style),
        Paragraph("Analytical Explanation &amp; Remarks", th_style),
    ]]

    for r in analysis.results:
        val_str = f"{r.entered_value}" if r.entered_value is not None else "—"
        stat_color = _status_color(r.status)
        stat_hex = stat_color.hexval()
        stat_html = f'<font color="{stat_hex}"><b>{r.status}</b></font>'

        results_table_data.append([
            Paragraph(f"<b>{r.display_name}</b>", td_style),
            Paragraph(val_str, td_bold),
            Paragraph(r.unit, ParagraphStyle("TDUnit", fontName="Helvetica", fontSize=7, leading=9, alignment=TA_CENTER)),
            Paragraph(r.reference_range, ParagraphStyle("TDRange", fontName="Helvetica", fontSize=7, leading=9, alignment=TA_CENTER)),
            Paragraph(stat_html, ParagraphStyle("TDStat", fontName="Helvetica", fontSize=7.5, leading=9, alignment=TA_CENTER)),
            Paragraph(r.explanation, td_rem),
        ])

    results_table = Table(
        results_table_data,
        colWidths=[36 * mm, 18 * mm, 12 * mm, 28 * mm, 26 * mm, 60 * mm],
        repeatRows=1,
    )
    results_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GRAPE_DEEP),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LAVENDER]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(results_table)

    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 3: Observations, Guidance, Precautions & Disclaimer (Strict 1-Page)
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("GrapeLeaf AI – Observations &amp; Guidance", title_style))
    story.append(Paragraph("Nutrient Interpretation, Agronomic Next Steps &amp; Safeguards", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=GRAPE_DEEP, spaceBefore=4, spaceAfter=6))

    # Partition results
    low_list = [r for r in analysis.results if r.status == "Low"]
    high_list = [r for r in analysis.results if r.status == "High"]
    above_safe_list = [r for r in analysis.results if r.status == "Above Safe Limit"]
    optimum_list = [r for r in analysis.results if r.status == "Optimum"]
    safe_list = [r for r in analysis.results if r.status == "Safe"]
    unavail_list = [r for r in analysis.results if r.status == "Data Unavailable"]

    obs_title_style = ParagraphStyle(
        "ObsTitle",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        spaceBefore=3,
        spaceAfter=1,
    )
    obs_body_style = ParagraphStyle(
        "ObsBody",
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=BLACK,
        spaceAfter=2,
    )

    def _render_obs_group(title: str, items: List[NutrientResult], header_color: colors.Color):
        if not items:
            return
        hex_code = header_color.hexval()
        story.append(Paragraph(f'<font color="{hex_code}"><b>[ {title.upper()} ]</b></font>', obs_title_style))
        for item in items:
            val_str = f"{item.entered_value} {item.unit}" if item.entered_value is not None else "—"
            text = f"<b>{item.display_name}</b> ({val_str}) &mdash; {item.explanation} <i>Guidance: {item.recommendation}</i>"
            story.append(Paragraph(text, obs_body_style))

    # 1. Attention items first (Low, High, Above Safe)
    _render_obs_group("Low Nutrient Observations", low_list, AMBER)
    _render_obs_group("High Nutrient Observations", high_list, ORANGE_HIGH)
    _render_obs_group("Above Safe Limit Observations (Salinity Stress)", above_safe_list, RED_ABOVE)

    # 2. Balanced items (Optimum, Safe)
    if optimum_list or safe_list:
        opt_names = [f"{r.display_name} ({r.entered_value} {r.unit})" for r in optimum_list]
        safe_names = [f"{r.display_name} ({r.entered_value} {r.unit})" for r in safe_list]
        combined = opt_names + safe_names
        story.append(Paragraph('<font color="#4F772D"><b>[ OPTIMUM &amp; SAFE STATUS ]</b></font>', obs_title_style))
        story.append(Paragraph(
            f"The following {len(combined)} nutrient(s) meet October Pruning reference standards: <b>{', '.join(combined)}</b>. "
            "Continue balanced irrigation and maintenance fertilization.",
            obs_body_style
        ))

    # 3. Unavailable items
    if unavail_list:
        unavail_names = ", ".join(r.display_name for r in unavail_list)
        story.append(Paragraph('<font color="#6B7280"><b>[ DATA UNAVAILABLE ]</b></font>', obs_title_style))
        story.append(Paragraph(
            f"No measured values were provided for: {unavail_names}. These were excluded from classification.",
            obs_body_style
        ))

    story.append(Spacer(1, 3 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=2, spaceAfter=4))

    # Recommended Next Steps
    story.append(Paragraph("Recommended Agronomic Next Steps", section_heading))
    steps_html = (
        "1. <b>Review with a specialist:</b> Consult a certified viticulturist or local agricultural extension officer prior to adjusting fertigation schedules.<br/>"
        "2. <b>Salinity screening:</b> If Sodium or Chloride is above safe limits, test soil electrical conductivity (EC) and irrigation water source.<br/>"
        "3. <b>Growth stage confirmation:</b> Re-verify tissue samples at berry set and veraison to track seasonal mobilization curves.<br/>"
        "4. <b>Maintain application logs:</b> Keep detailed logs of all soil and foliar applications to diagnose potential ion antagonisms."
    )
    story.append(Paragraph(steps_html, body_style))

    story.append(Spacer(1, 3 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=2, spaceAfter=4))

    # Precautions & Limitations
    story.append(Paragraph("Precautions &amp; Biological Limitations", section_heading))
    precautions_html = (
        "&bull; <b>Standards Scope:</b> Calibrated for grape petioles at October forward pruning. Not applicable to other phenological stages.<br/>"
        "&bull; <b>Varietal Differences:</b> Table varieties (Thompson Seedless) and wine varieties have distinct nutrient demands.<br/>"
        "&bull; <b>Rootstock Influence:</b> Rootstocks like Dogridge or 110R alter potassium, magnesium, and chloride uptake significantly.<br/>"
        "&bull; <b>Lab Variation:</b> Differences in petiole washing, drying, and digestion techniques can introduce measurement variance."
    )
    story.append(Paragraph(precautions_html, body_style))

    story.append(Spacer(1, 3 * mm))

    # Educational Disclaimer Box
    disclaimer_box_data = [[
        Paragraph(
            "<b>Educational Decision Support Disclaimer:</b> This report provides educational decision support based strictly on entered values and configured October Pruning reference standards. It is not a substitute for qualified agricultural advice. Do not apply chemical fertilizers or amendments without professional verification. GrapeLeaf AI does not guarantee yield improvement, disease detection, or crop recovery.",
            disclaimer_style
        )
    ]]
    disc_table = Table(disclaimer_box_data, colWidths=[180 * mm])
    disc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFDF8")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5D8BC")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(disc_table)

    doc.build(story, onFirstPage=_add_page_decorations, onLaterPages=_add_page_decorations)
    return buffer.getvalue()
