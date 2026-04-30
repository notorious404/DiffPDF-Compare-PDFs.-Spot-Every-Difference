from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import json
from typing import Dict, Any


class PDFReportGenerator:
    def __init__(self, output_path: str):
        self.doc = SimpleDocTemplate(output_path, pagesize=A4)
        self.story = []
        self.styles = getSampleStyleSheet()

    def create_comparison_report(self, comparison_result: Dict[str, Any]):
        self._add_title()
        self._add_document_list(comparison_result)
        self._add_comparison_table(comparison_result)
        self._add_insights_section(comparison_result)
        self.doc.build(self.story)

    def _add_title(self):
        title = Paragraph("PDF Comparison Report", self.styles["Title"])
        self.story.append(title)
        self.story.append(Spacer(1, 18))

    def _add_document_list(self, result: Dict[str, Any]):
        pdf_names = result["pdf_names"]
        text = "Compared Documents:<br/>" + "<br/>".join(
            [f"- {name}" for name in pdf_names]
        )
        para = Paragraph(text, self.styles["Normal"])
        self.story.append(para)
        self.story.append(Spacer(1, 12))

    def _add_comparison_table(self, result: Dict[str, Any]):
        """Create comparison table with real wrapped cells."""
        raw_comp = result["comparison"]["raw_comparison"]

        try:
            comp = json.loads(raw_comp)
            similarities = comp.get("similarities", [])
            differences = comp.get("differences", [])
            score = comp.get("overall_similarity_score", "N/A")
        except Exception:
            similarities = []
            differences = []
            score = "N/A"

        styles = getSampleStyleSheet()
        cell_style = ParagraphStyle(
            "Cell",
            parent=styles["Normal"],
            fontSize=9,
            leading=11,
        )

        def P(text: str) -> Paragraph:
            return Paragraph(str(text).replace("\n", "<br/>"), cell_style)

        data = [
            [P("Aspect"), P("Details")],
            [P("Overall Similarity Score"), P(str(score))],
        ]

        if similarities:
            sim_text = "; ".join(similarities)
            data.append([P("Similarities"), P(sim_text)])

        if differences:
            lines = []
            for d in differences:
                cat = d.get("category", "Difference")
                docs = d.get("documents", {})
                docs_str = "; ".join([f"{k}: {v}" for k, v in docs.items()])
                lines.append(f"{cat} -> {docs_str}")
            diff_text = "<br/>".join(lines)
            data.append([P("Differences (top)"), P(diff_text)])

        table = Table(
            data,
            colWidths=[120, 380],
            repeatRows=1,
        )

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ]
            )
        )

        self.story.append(table)
        self.story.append(Spacer(1, 18))

    def _add_insights_section(self, result: Dict[str, Any]):
        title = Paragraph("Key Insights & Recommendations", self.styles["Heading2"])
        self.story.append(title)
        self.story.append(Spacer(1, 8))

        insights_text = result["insights"].get("insights", "")
        para_style = ParagraphStyle(
            "Insights",
            parent=self.styles["Normal"],
            fontSize=10,
            leading=12,
            spaceAfter=10,
        )
        para = Paragraph(insights_text.replace("\n", "<br/>"), para_style)
        self.story.append(para)
