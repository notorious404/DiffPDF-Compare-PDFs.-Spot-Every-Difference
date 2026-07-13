from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
import os
import json
import difflib
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from pdf_processor import PDFProcessor
from chatgpt_comparator import ChatGPTComparator
from config import GEMINI_API_KEY, MODEL_NAME, MAX_TOKENS, TEMPERATURE

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'input_pdfs')
app.config['REPORT_FOLDER'] = os.path.join(BASE_DIR, 'output_reports')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)
REPORTS = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/compare', methods=['POST'])
def compare():
    try:
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'Two PDF files are required'}), 400

        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Please select both PDF files'}), 400

        name1 = secure_filename(file1.filename)
        name2 = secure_filename(file2.filename)
        if not name1.lower().endswith('.pdf') or not name2.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are supported'}), 400

        path1 = os.path.join(app.config['UPLOAD_FOLDER'], name1)
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], name2)

        file1.save(path1)
        file2.save(path2)

        text1 = PDFProcessor.extract_text_from_pdf(path1)
        text2 = PDFProcessor.extract_text_from_pdf(path2)
        if not text1 and not text2:
            return jsonify({'error': 'Could not extract text from either PDF'}), 422

        diff_rows = build_line_diff(text1, text2)
        result = {
            'pdf_names': [name1, name2],
            'summaries': {},
            'comparison': {'raw_comparison': diff_rows},
            'insights': {'insights': build_basic_insights(diff_rows, name1, name2)},
        }

        if GEMINI_API_KEY:
            result['insights']['insights'] = build_ai_insights(text1, text2, name1, name2, diff_rows)

        report_id = uuid.uuid4().hex
        report_path = os.path.join(app.config['REPORT_FOLDER'], f'comparison_{report_id}.pdf')
        create_diff_report(report_path, result)
        REPORTS[report_id] = report_path
        result['report_url'] = f'/api/report/{report_id}'

        return jsonify(result)
    except Exception as e:
        app.logger.exception('PDF comparison failed')
        return jsonify({'error': f'Comparison failed: {e}'}), 500


@app.route('/api/report/<report_id>', methods=['GET'])
def download_report(report_id):
    report_path = REPORTS.get(report_id)
    if not report_path or not os.path.exists(report_path):
        return jsonify({'error': 'Report not found. Please run the comparison again.'}), 404

    return send_file(
        report_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='pdf-comparison-report.pdf',
    )


def build_line_diff(text1, text2):
    lines1 = normalize_lines(text1)
    lines2 = normalize_lines(text2)
    matcher = difflib.SequenceMatcher(a=lines1, b=lines2)
    rows = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        left = lines1[i1:i2]
        right = lines2[j1:j2]

        if tag == 'equal':
            rows.extend({'original': line, 'modified': line, 'status': 'unchanged'} for line in left)
        elif tag == 'delete':
            rows.extend({'original': line, 'modified': '', 'status': 'removed'} for line in left)
        elif tag == 'insert':
            rows.extend({'original': '', 'modified': line, 'status': 'added'} for line in right)
        elif tag == 'replace':
            paired = min(len(left), len(right))
            for index in range(paired):
                rows.append({
                    'original': left[index],
                    'modified': right[index],
                    'status': 'modified',
                })
            rows.extend({'original': line, 'modified': '', 'status': 'removed'} for line in left[paired:])
            rows.extend({'original': '', 'modified': line, 'status': 'added'} for line in right[paired:])

    return rows


def normalize_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def build_basic_insights(diff_rows, name1, name2):
    counts = {'added': 0, 'removed': 0, 'modified': 0, 'unchanged': 0}
    for row in diff_rows:
        counts[row['status']] = counts.get(row['status'], 0) + 1

    total_changes = counts['added'] + counts['removed'] + counts['modified']
    return (
        f"- Compared {name1} with {name2}.\n"
        f"- Found {total_changes} changed lines: {counts['added']} added, "
        f"{counts['removed']} removed, and {counts['modified']} modified.\n"
        f"- {counts['unchanged']} lines matched exactly after PDF text extraction."
    )


def build_ai_insights(text1, text2, name1, name2, diff_rows):
    try:
        comparator = ChatGPTComparator(
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        changed_sample = [
            row for row in diff_rows
            if row['status'] in {'added', 'removed', 'modified'}
        ][:80]
        prompt = f"""
Compare these two PDF text extracts and summarize the important differences.

Document A: {name1}
Document B: {name2}

Changed line sample:
{json.dumps(changed_sample, ensure_ascii=False)}

Document A excerpt:
\"\"\"{text1[:4000]}\"\"\"

Document B excerpt:
\"\"\"{text2[:4000]}\"\"\"

Return concise plain-text bullet points only.
"""
        return comparator._generate_text(prompt)
    except Exception as e:
        app.logger.warning('Gemini insights failed: %s', e)
        return build_basic_insights(diff_rows, name1, name2)


def create_diff_report(report_path, result):
    styles = getSampleStyleSheet()
    normal = styles['Normal']
    small = ParagraphStyle('Small', parent=normal, fontSize=8, leading=10)
    heading = styles['Heading2']
    doc = SimpleDocTemplate(
        report_path,
        pagesize=landscape(A4),
        rightMargin=24,
        leftMargin=24,
        topMargin=24,
        bottomMargin=24,
    )
    story = []
    diff_rows = result['comparison']['raw_comparison']
    names = result['pdf_names']
    counts = {'added': 0, 'removed': 0, 'modified': 0, 'unchanged': 0}
    for row in diff_rows:
        counts[row['status']] = counts.get(row['status'], 0) + 1

    story.append(Paragraph('PDF Comparison Report', styles['Title']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f'Document A: {names[0]}', normal))
    story.append(Paragraph(f'Document B: {names[1]}', normal))
    story.append(Paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', normal))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Summary', heading))
    story.append(Paragraph(
        f"Added: {counts['added']} | Removed: {counts['removed']} | "
        f"Modified: {counts['modified']} | Unchanged: {counts['unchanged']}",
        normal,
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph('Insights', heading))
    story.append(Paragraph(escape_report_text(result['insights'].get('insights', '')), normal))
    story.append(Spacer(1, 14))
    story.append(Paragraph('Changes Found', heading))

    changed_rows = [row for row in diff_rows if row.get('status') != 'unchanged']
    if not changed_rows:
        story.append(Paragraph('No added, removed, or modified lines were found.', normal))
        doc.build(story)
        return

    table_data = [[
        Paragraph('<b><font color="#ffffff">#</font></b>', small),
        Paragraph('<b><font color="#ffffff">Status</font></b>', small),
        Paragraph('<b><font color="#ffffff">Document A</font></b>', small),
        Paragraph('<b><font color="#ffffff">Document B</font></b>', small),
    ]]
    for index, row in enumerate(changed_rows[:250], start=1):
        status = row.get('status', '').lower()
        original = format_report_change(row.get('original', ''), status, 'original')
        modified = format_report_change(row.get('modified', ''), status, 'modified')
        table_data.append([
            Paragraph(str(index), small),
            Paragraph(f'<b>{escape_report_text(row["status"].title())}</b>', small),
            Paragraph(original, small),
            Paragraph(modified, small),
        ])

    table = Table(table_data, colWidths=[32, 70, 320, 320], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#111827')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    for row_index, row in enumerate(changed_rows[:250], start=1):
        status = row.get('status')
        if status == 'added':
            table.setStyle(TableStyle([('BACKGROUND', (0, row_index), (-1, row_index), colors.HexColor('#dcfce7'))]))
        elif status == 'removed':
            table.setStyle(TableStyle([('BACKGROUND', (0, row_index), (-1, row_index), colors.HexColor('#fee2e2'))]))
        elif status == 'modified':
            table.setStyle(TableStyle([('BACKGROUND', (0, row_index), (-1, row_index), colors.HexColor('#fef3c7'))]))
    story.append(table)

    if len(changed_rows) > 250:
        story.append(Spacer(1, 8))
        story.append(Paragraph('Only the first 250 changed rows are included in this PDF report.', normal))

    doc.build(story)


def format_report_change(value, status, side):
    text = escape_report_text(value)
    if not text:
        return ''

    if status == 'added' and side == 'modified':
        return f'<b><font color="#166534">{text}</font></b>'
    if status == 'removed' and side == 'original':
        return f'<b><font color="#991b1b">{text}</font></b>'
    if status == 'modified':
        return f'<b><font color="#92400e">{text}</font></b>'
    return text


def escape_report_text(value):
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=False, port=port, use_reloader=False)
