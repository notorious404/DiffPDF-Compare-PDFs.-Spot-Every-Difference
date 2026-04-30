# 📄 DiffPDF — Compare PDFs. Spot Every Difference.

## 🎯 What Is DiffPDF?

DiffPDF is a modern, browser-based PDF comparison tool that lets you upload two PDF files and instantly visualize the differences between them. Whether you're a developer reviewing document changes, a legal professional tracking contract revisions, or a student comparing essay drafts — DiffPDF makes it effortless.

> **Built as a frontend development showcase project** — demonstrating advanced UI/UX skills, modern JavaScript patterns, responsive design, and polished micro-interactions.

---

## ✨ Features

### 🔍 Core Functionality
- **Side-by-Side Diff View** — Compare two PDFs in synchronized, scrollable panels
- **Unified View Toggle** — Switch between side-by-side and unified diff display
- **Inline Character Diff** — Highlights exact characters that changed within a line
- **Color-Coded Highlights** — Green for additions, red for deletions, yellow for modifications
- **Line Numbers** — Monospace-aligned line references for both documents
- **Search in Diff** — Filter visible lines by keyword

### 🎨 UI/UX Highlights
- **Drag & Drop Upload** — Smooth drag-and-drop with animated feedback states
- **Live Stats Dashboard** — Animated counters for added, removed, and modified lines
- **Synchronized Scrolling** — Both panels scroll in perfect sync
- **Scroll-Reveal Animations** — Sections animate in as you scroll using IntersectionObserver
- **Responsive Design** — Fully optimized for mobile, tablet, and desktop
- **Loading States** — Animated progress ring with live status messages during processing

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Styling** | Custom CSS Design System + CSS Variables |
| **Animations** | CSS @keyframes + requestAnimationFrame |
| **PDF Parsing** | pdf.js / pdfplumber |
| **Diff Algorithm** | difflib / jsdiff |
| **Deployment** | Vercel / Netlify |

---

## 🚀 Getting Started

### Prerequisites
- Node.js v18+ (if applicable)
- Python 3.8+ (if applicable)
- A modern browser (Chrome, Firefox, Safari, Edge)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/notorious404/PDF-COMPARSION-APP-.git
cd PDF-COMPARSION-APP-

# 2. Install dependencies
npm install
# or
pip install -r requirements.txt

# 3. Start the development server
npm run dev
# or
python app.py
```

### Usage

```
1. Open the app in your browser (http://localhost:3000 or http://localhost:5000)
2. Upload Document A (Original) in the left drop zone
3. Upload Document B (Modified) in the right drop zone
4. Click "Compare Documents"
5. Review highlighted differences in the results panel
```

---
## 🧠 How It Works

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Upload 2   │────▶│  Extract text    │────▶│  Run diff    │
│  PDF files  │     │  from each PDF   │     │  algorithm   │
└─────────────┘     └──────────────────┘     └──────┬───────┘
                                                     │
                    ┌──────────────────┐             ▼
                    │  Render colored  │◀────  ┌──────────────┐
                    │  diff in panels  │       │  Map changes │
                    └──────────────────┘       │  to lines    │
                                               └──────────────┘
```

1. **Upload** — User selects or drags two PDF files
2. **Parse** — Text content is extracted from both PDFs page by page
3. **Diff** — A line-by-line diff algorithm identifies additions, deletions, and modifications
4. **Render** — Results are displayed in a color-coded, synchronized side-by-side view

---

## ⚡ Performance

- Instant diff results for documents up to 50 pages
- Scroll-sync uses a guard-flag pattern to prevent event loop conflicts
- Animations use `transform` and `opacity` only — no layout-triggering properties
- IntersectionObserver used instead of scroll listeners for reveal effects

---

## 🎨 Design Decisions

| Decision | Reasoning |
|---|---|
| Dark theme by default | Reduces eye strain for long document reviews |
| Monospace font for diff | Aligns characters for easier line-by-line reading |
| Synchronized scrolling | Keeps context between documents at all times |
| Animated stat counters | Draws attention to the key output data immediately |
| Side-by-side default | More intuitive than unified view for non-technical users |

---

## 🗺️ Roadmap

- [ ] Export diff as PDF or HTML report
- [ ] Page-by-page navigation for multi-page documents
- [ ] Image/visual diff mode (not just text)
- [ ] Dark/light theme toggle
- [ ] Shareable diff links (via URL hash)
- [ ] Keyboard shortcuts for power users

---

## 🤝 Contributing

Contributions are welcome! Here's how:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
# Open a Pull Request
```

Please follow existing code style and add comments for any new logic.

---

## 👨‍💻 Author

**Shantanu Yadav**  
Frontend Developer & Full Stack Builder
---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

<div align="center">

**If this project helped you or impressed you, drop a ⭐ — it means a lot!**

Made with 💜 by [Shantanu Yadav](https://github.com/notorious404)

</div>
