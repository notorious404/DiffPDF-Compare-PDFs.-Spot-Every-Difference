from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime

from pdf_processor import PDFProcessor
from chatgpt_comparator import ChatGPTComparator
from report_generator import PDFReportGenerator
from config import MODEL_NAME, MAX_TOKENS, TEMPERATURE

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'input_pdfs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('output_reports', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/compare', methods=['POST'])
def compare():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Two files are required'}), 400
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    
    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    path1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename))
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename))
    
    file1.save(path1)
    file2.save(path2)
    
    pdf_contents = {}
    pdf_contents[secure_filename(file1.filename)] = PDFProcessor.extract_text_from_pdf(path1)
    pdf_contents[secure_filename(file2.filename)] = PDFProcessor.extract_text_from_pdf(path2)
    
    comparator = ChatGPTComparator(
        model_name=MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    
    try:
        comparison_result = comparator.compare_pdfs(pdf_contents)
        
        # Parse nested json strings
        for k, v in comparison_result['summaries'].items():
            try:
                comparison_result['summaries'][k] = json.loads(v)
            except:
                pass
                
        try:
            comparison_result['comparison']['raw_comparison'] = json.loads(comparison_result['comparison']['raw_comparison'])
        except:
            pass
            
        return jsonify(comparison_result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
