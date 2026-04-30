import os
import json
from datetime import datetime

import streamlit as st

from pdf_processor import PDFProcessor
from chatgpt_comparator import ChatGPTComparator
from report_generator import PDFReportGenerator
from utils import ensure_directories
from config import OPENAI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE

st.set_page_config(page_title="PDF Comparison App", layout="wide")
ensure_directories()

st.title("📄 AI PDF Comparison App")
st.write(
    "Upload multiple PDFs, they will be saved into **input_pdfs/**, "
    "then compared with **ChatGPT**, and a PDF report will be generated."
)

with st.sidebar:
    st.header("Settings")
    api_status = "✅ API key loaded" if OPENAI_API_KEY else "⚠️ No API key found"
    st.caption(api_status)

    temperature_ui = st.slider("Model temperature", 0.0, 1.0, TEMPERATURE, 0.05)
    max_tokens_ui = st.slider("Max tokens per call", 512, 8192, MAX_TOKENS, 256)

    st.markdown("---")
    st.caption("For very long PDFs, start with 2–3 documents for speed.")

uploaded_files = st.file_uploader(
    "Upload PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    help="You can select multiple PDFs at once.",
)

col1, col2 = st.columns([1, 2])
with col1:
    run_button = st.button("🚀 Run comparison", use_container_width=True)
with col2:
    download_placeholder = st.empty()

if run_button:
    if not uploaded_files:
        st.error("Please upload at least two PDF files.")
    elif len(uploaded_files) < 2:
        st.error("Please upload at least two PDFs to compare.")
    elif not OPENAI_API_KEY:
        st.error("OpenAI API key is missing. Set it in your .env file.")
    else:
        pdf_contents = {}
        st.info("Saving files to input_pdfs/ and extracting text...")
        total = len(uploaded_files)
        progress = st.progress(0.0)

        # save uploads into input_pdfs/ and read from disk
        for idx, f in enumerate(uploaded_files, start=1):
            safe_name = f.name.replace(" ", "_")
            save_path = os.path.join("input_pdfs", safe_name)

            with open(save_path, "wb") as out_file:
                out_file.write(f.getbuffer())

            text = PDFProcessor.extract_text_from_pdf(save_path)
            pdf_contents[safe_name] = text

            progress.progress(idx / total)

        st.info("Running ChatGPT comparison...")
        comparator = ChatGPTComparator(
            model_name=MODEL_NAME,
            temperature=temperature_ui,
            max_tokens=max_tokens_ui,
        )

        with st.spinner("Comparing documents with ChatGPT..."):
            comparison_result = comparator.compare_pdfs(pdf_contents)

        st.success("Comparison completed.")

        st.subheader("Summaries")
        for name, summary_json in comparison_result["summaries"].items():
            with st.expander(name, expanded=False):
                try:
                    parsed = json.loads(summary_json)
                    st.json(parsed)
                except Exception:
                    st.write(summary_json)

        st.subheader("Detailed comparison")
        try:
            raw_comp = comparison_result["comparison"]["raw_comparison"]
            parsed_comp = json.loads(raw_comp)
            st.json(parsed_comp)
        except Exception:
            st.write(comparison_result["comparison"]["raw_comparison"])

        st.subheader("Insights")
        st.markdown(comparison_result["insights"]["insights"])

        st.info("Generating PDF report...")

        # ---- dynamic report name using PDF names ----
        pdf_names = comparison_result["pdf_names"]
        base_name = "_VS_".join([os.path.splitext(n)[0] for n in pdf_names])
        base_name = base_name[:120]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("output_reports", exist_ok=True)
        report_path = f"output_reports/{base_name}_{timestamp}.pdf"
        # ---------------------------------------------

        generator = PDFReportGenerator(report_path)
        generator.create_comparison_report(comparison_result)

        with open(report_path, "rb") as f:
            download_placeholder.download_button(
                label="⬇️ Download comparison report",
                data=f,
                file_name=os.path.basename(report_path),
                mime="application/pdf",
                use_container_width=True,
            )

        st.success("Report ready. PDFs are stored in input_pdfs/ and report in output_reports/.")
