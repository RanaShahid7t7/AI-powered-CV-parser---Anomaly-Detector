### CV Parser & Anomaly Detector

A simple Streamlit app and companion notebooks to extract key fields from CV/resume PDFs and flag anomalies. It parses PDFs to pull name, email, phone, education, experience, and skills, then saves consolidated results to an Excel file for review.

### Features
- **PDF parsing**: Uses `pdfplumber` to extract text from uploaded PDFs
- **Field extraction**: Regex-based extraction for email, phone, name (first line), education, experience, and skills
- **Anomaly detection**: Rule-based checks for missing/invalid fields
- **Excel export**: Appends results to `all_cvs_dataset.xlsx` and provides a download button
- **Notebooks**: Step-by-step exploration and a sample pipeline for a single CV

### Project Structure
- `app.py`: Streamlit UI to upload multiple PDFs and export consolidated results
- `project.ipynb`: Clean pipeline for a single CV with validation and Excel export
- `prroject.ipynb`: Earlier exploration notebook for parsing and basic checks
- `CVs/`: Sample PDFs
- `all_cvs_dataset.xlsx`: Output file produced by the app (created on first run)

### Requirements
- Python 3.9+ (Windows compatible)
- Core packages:
  - `streamlit`
  - `pdfplumber`
  - `pandas`
  - `openpyxl`

### Installation
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, install directly:
```bash
pip install streamlit pdfplumber pandas openpyxl
```

### How to Run (App)
```bash
streamlit run app.py
```

Steps in the UI:
1. Upload one or more CV PDFs
2. Review extracted data in the on-screen table
3. Download the updated Excel via the provided button

The app saves/appends results to `all_cvs_dataset.xlsx` in the project root.

### How It Works (Brief)
1. Text extraction via `pdfplumber`
2. Regex rules pull fields (email, phone, etc.) and heuristics set the name from the first line
3. Rule-based anomaly checks flag missing/invalid fields
4. Results are combined into a DataFrame and written to Excel

### Notes & Limitations
- Regex rules are heuristic and may miss fields depending on CV formatting
- The first-line-as-name heuristic may fail for some templates
- Education/experience/skills extraction rely on simple keyword-based matching
- Improve accuracy by adding NLP-based parsing or template-aware rules

### Troubleshooting
- If Excel writing fails, ensure `openpyxl` is installed and the file is not open in Excel
- If PDFs fail to parse, verify the PDFs contain selectable text (not just images); for scans, add OCR (e.g., `pytesseract`)

### License
This project is provided as-is for educational purposes. Add a license if you plan to distribute.


