#!/usr/bin/env python3

import os
from datetime import datetime

from pdf_processor import PDFProcessor
from chatgpt_comparator import ChatGPTComparator
from report_generator import PDFReportGenerator
from utils import ensure_directories


def main():
    ensure_directories()
    print("Starting PDF Comparison (CLI mode)...")

    pdf_contents = PDFProcessor.process_pdfs_folder("input_pdfs")
    if len(pdf_contents) < 2:
        print("Need at least two PDFs in input_pdfs/ to compare.")
        return

    print(f"Found {len(pdf_contents)} PDF(s). Running comparison...")

    comparator = ChatGPTComparator()
    comparison_result = comparator.compare_pdfs(pdf_contents)

    # ---- dynamic report name using PDF names ----
    pdf_names = comparison_result["pdf_names"]
    base_name = "_VS_".join([os.path.splitext(n)[0] for n in pdf_names])
    base_name = base_name[:120]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("output_reports", exist_ok=True)
    output_filename = f"output_reports/{base_name}_{timestamp}.pdf"
    # ---------------------------------------------

    generator = PDFReportGenerator(output_filename)
    generator.create_comparison_report(comparison_result)
    print(f"Report generated: {output_filename}")


if __name__ == "__main__":
    main()
