# 📄 PDF Table Comparison App

A powerful **PDF Table Comparison Application** built to compare tables extracted from two PDF documents and highlight **differences, mismatches, and structural changes** in a clear and readable format.


# ABOUT
## 🧑‍💻 Author

Shantanu Yadav
B.Tech Computer Science Student

## 📜 License

This project is licensed under the MIT License.
---

## 🚀 Features

- 📤 Upload **two PDF documents** for comparison
- 🔍 Row-wise and column-wise table comparison
- 📊 Detects:
  - Missing rows and columns
  - Value mismatches
  - Structural differences
- 🧠 Intelligent table normalization for fair comparison
- 📈 Supports multi-page tables
- 📄 Generates a **detailed PDF mismatch report**
- 🗂️ Clean and audit-friendly output

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Interactive web interface
- **Pandas** – Data handling and comparison
- **OpenAI API** – Intelligent difference analysis
- **ReportLab** – PDF comparison report generation

---

## 📌 Use Cases

- Financial statement comparison
- Audit and compliance validation
- Contract and legal document review
- Report version comparison
- Academic and research analysis

---

## 📂 Project Workflow

1. Upload two PDF files
2. Load pre-extracted tables from each document
3. Normalize table structure and values
4. Compare tables row-wise and column-wise
5. Detect mismatches and missing data
6. Generate a detailed comparison PDF report

---

## 📄 Output

- Highlighted mismatches and differences
- Structured comparison tables
- Auto-generated PDF comparison report
- Clear, readable, review-ready format

---

## 🧩 Scope Clarification

- ✅ This project handles **only PDF table comparison**
- 🔗 Extraction is managed in a **separate repository**

---

## ⚙️ Installation

-git clone https://github.com/your-username/pdf-table-comparison-app.git
-cd pdf-table-comparison-app
-pip install -r requirements.txt

## ▶️ Run the App
-streamlit run app.py

## 🔐 Environment Variables

-Create a .env file and add:

-OPENAI_API_KEY=your_api_key_here

## 📌 Limitations

-Comparison accuracy depends on extracted table quality

-Large PDFs may increase processing time

-Extremely inconsistent table structures may require manual review

# END



