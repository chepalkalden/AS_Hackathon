# 🚀 Automated File Processing & Data Transformation Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)
![Automation](https://img.shields.io/badge/Process-Automation-orange)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 🎯 Key Capabilities

### 1. OCR Extractor (`1_OCR_Extractor.py`)
- **Offline Text & Layout Extraction**: Uses Tesseract OCR and advanced OpenCV preprocessing to extract text while maintaining spatial structures (tables, multi-column layouts).
- **Format Support**: Processes both image files (`.jpg`, `.png`) and `.pdf` documents using PyMuPDF.
- **Auto Spell Checker**: Uses `autocorrect` and `textblob` to dynamically fix characters that OCR might miss or misinterpret.
- **Export Options**: Export extracted text directly to TXT, Excel, Microsoft Word, or PDF.

### 2. Excel Mapper (`2_Excel_Mapper.py`)
- **Dynamic Field Mapping**: Automatically identifies and transforms account structure columns using string matching.
- **ETL Rollup Processing**: Fetches records from an Oracle Database logic and securely maps data across multiple configurations (`TX`, `IL`, `BBA`).
- **Interactive UI Preview**: Review transformed payload grids natively via dataframes before finalizing submissions.

---

## 🛠️ How to Setup (For New Users)

Follow these instructions to get the application running on your local machine.

### Step 1: Clone the Repository
Open a terminal and clone the repository:
```bash
git clone <your-repo-url>
cd "AS_Hackathon/codes"
```

### Step 2: Set up a Virtual Environment (Recommended)
It is highly recommended to construct a Python virtual environment to house dependencies:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Install all the needed packages listed in the `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 4: Install System Packages (Tesseract OCR)
Because the OCR extraction relies on the Tesseract engine, you must install Tesseract locally:
1. **Windows**: Download the Windows installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and install it.
   - *Note: The code automatically searches common Windows paths (e.g., `C:\Program Files\Tesseract-OCR\tesseract.exe`). If you install it elsewhere, add it to your system PATH.*
2. **Mac**: `brew install tesseract`
3. **Linux**: `sudo apt-get install tesseract-ocr`

### Step 5: Start the Application
Navigate into the `codes` directory and launch the Streamlit frontend:
```bash
cd codes
streamlit run Home.py
```

The application will launch automatically in your web browser!

---

## 💻 Tech Stack
- 🐍 **Python** (Core backend)
- 🎈 **Streamlit** (Web application framework)
- 👁️ **PyTesseract / OpenCV** (Spatial Document OCR)
- 🐼 **Pandas** (Data manipulation)
- 🔤 **RapidFuzz / Autocorrect / TextBlob** (Text correction and fuzzy matching)
- 📊 **OpenPyXL / Python-Docx / FPDF** (Document generation)
