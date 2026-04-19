import streamlit as st
from PIL import Image
import io
import pandas as pd
import numpy as np
import pytesseract
from docx import Document
from fpdf import FPDF
import shutil
import os

# 1. PAGE CONFIG & STATE
st.set_page_config(page_title="Tesseract Vision OCR", layout="wide")

if 'extracted_text' not in st.session_state:
    st.session_state['extracted_text'] = ""

# Auto-detect Tesseract to prevent offline breaking
try:
    tess_path = shutil.which("tesseract")
    if not tess_path:
        common_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'E:\DevTools\Tesseract\tesseract.exe',
            r'E:\Tesseract-OCR\tesseract.exe',
            r'D:\Tesseract-OCR\tesseract.exe'
        ]
        for p in common_paths:
            if os.path.exists(p):
                tess_path = p
                break
    if tess_path:
        pytesseract.pytesseract.tesseract_cmd = tess_path
except:
    pass

# 2. UI LAYOUT & WORKFLOW
st.title("OCR Extractor (Tesseract Spatial Engine)")

st.subheader("Step 1: Upload File")
uploaded_file = st.file_uploader("Upload Image or PDF", type=["jpg", "jpeg", "png", "pdf"])

images_to_process = []

if uploaded_file:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        try:
            import fitz  # PyMuPDF
            file_bytes = uploaded_file.read()
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            st.info(f"Loaded PDF Document with {len(doc)} pages.")
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                matrix = fitz.Matrix(300/72, 300/72)
                pix = page.get_pixmap(matrix=matrix)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images_to_process.append(img)
            doc.close()
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    else:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            images_to_process.append(img)
        except Exception as e:
            st.error(f"Error reading Image: {e}")
            
    if images_to_process:
        st.image(images_to_process[0], caption=f"Preview (Page 1 of {len(images_to_process)})", width=500)

# Step 2 — Extraction
st.markdown("---")
if images_to_process:
    st.subheader("Step 2: Run Extraction")
    if st.button("Extract Entire Document", type="primary"):
        with st.spinner("Tesseract is calculating spatial boundaries & generating layout..."):
            try:
                all_extracted_text = []
                
                for i, img in enumerate(images_to_process):
                    try:
                        import cv2
                        img_np = np.array(img.convert('RGB'))
                        
                        # 1. ENHANCED PREPROCESSING FOR BLURRY & LOW-CONTRAST IMAGES
                        # Convert to grayscale
                        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                        
                        # 2x Cubic Scaling increases pixel density, giving Tesseract's LSTM more data per character
                        gray = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
                        
                        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
                        # Fixes washed out/low-contrast text without destroying localized lighting
                        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                        contrast = clahe.apply(gray)
                        
                        # Unsharp Masking to crisp up blurry edges
                        blur = cv2.GaussianBlur(contrast, (5, 5), 0)
                        sharpened = cv2.addWeighted(contrast, 1.7, blur, -0.7, 0)
                        
                        # Clean up near-white background noise without destroying anti-aliased text edges
                        sharpened[sharpened > 210] = 255
                        
                        # Note: We purposely do NOT use a hard binarization (like Otsu) here! 
                        # Hard binarization snaps blurry grays to white, physically erasing parts of letters.
                        # Tesseract 4+ LSTM engines natively process grayscale and handle soft edges better.
                        processed_img = Image.fromarray(sharpened)
                    except ImportError:
                        processed_img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
                        
                    # 2. ALIGNED ENGINE CONFIGURATION
                    # --oem 1 (LSTM Engine only) reduces hallucinating other languages on blurry text
                    # --psm 4 (Assume single column of text of variable sizes) handles spacing/forms well
                    custom_config = r'-l eng --oem 1 --psm 4 -c preserve_interword_spaces=1 tessedit_char_blacklist=|_[]'
                    raw_text = pytesseract.image_to_string(processed_img, config=custom_config)
                    
                    # Auto Spell Checker (fixes missing characters and typos from OCR)
                    try:
                        from autocorrect import Speller
                        spell = Speller(lang='en')
                        def correct_text(text):
                            return spell(text)
                    except ImportError:
                        try:
                            from textblob import TextBlob
                            def correct_text(text):
                                return str(TextBlob(text).correct())
                        except ImportError:
                            st.toast("Auto Spell Checker: Install `autocorrect` via 'pip install autocorrect'", icon="⚠️")
                            def correct_text(text):
                                return text
                                
                    final_lines = []
                    in_table = False
                    
                    import re
                    for line in raw_text.split('\n'):
                        if not line.strip():
                            continue
                            
                        # Intelligent Spacing Split: Any gap larger than 3 spaces is visually interpreted as a new column cell
                        cells = re.split(r'\s{3,}', line.strip())
                        cells = [c.strip() for c in cells if c.strip() != ""]
                        
                        if not cells:
                            continue
                            
                        # Fix spelling/missing characters on each extracted cell
                        cells = [correct_text(c) for c in cells]
                            
                        # If a row only has 1 or 2 small chunks outside of the main grid body, treat it as a Markdown Header
                        if len(cells) <= 2 and not in_table:
                            title_text = " ".join(cells)
                            if len(final_lines) == 0:
                                final_lines.append(f"## {title_text}") 
                            else:
                                final_lines.append(f"**{title_text}**") 
                            final_lines.append("")
                        else:
                            in_table = True
                            final_lines.append(" | ".join(cells))
                    
                    page_content = "\n".join(final_lines)
                    if len(images_to_process) > 1:
                        all_extracted_text.append(f"## --- Page {i+1} ---\n\n{page_content}\n")
                    else:
                        all_extracted_text.append(page_content)
                        
                final_text = "\n".join(all_extracted_text)
                st.session_state['extracted_text'] = final_text
                st.success("Extraction Complete!")
                
            except Exception as e:
                st.error(f"Extraction failed! Internal Error: {str(e)}")

# Step 3 — Result
if st.session_state.get('extracted_text') or images_to_process:
    st.markdown("---")
    st.subheader("Step 3: Result Pad")
    
    tab1, tab2 = st.tabs(["📋 Extracted Text", "🖼️ Preview"])
    
    with tab1:
        st.text_area("Raw Extracted Data", key="extracted_text", height=500, label_visibility="collapsed")
        
    with tab2:
        if images_to_process:
            st.image(images_to_process[0], use_container_width=True, caption="Source Preview")

# Step 4 — Options & Actions
if st.session_state.get('extracted_text'):
    st.markdown("---")
    st.subheader("Step 4: Options & Actions")
    
    current_data = st.session_state['extracted_text']
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.download_button("📄 TXT", current_data, "extraction.txt", "text/plain", use_container_width=True)
    with col2:
        df = pd.DataFrame({"Data": current_data.split("\n")})
        excel_buf = io.BytesIO()
        df.to_excel(excel_buf, index=False, engine='openpyxl')
        st.download_button("📊 Excel", excel_buf.getvalue(), "extraction.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with col3:
        doc = Document()
        doc.add_paragraph(current_data)
        word_buf = io.BytesIO()
        doc.save(word_buf)
        st.download_button("📝 Word", word_buf.getvalue(), "extraction.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with col4:
        pdf_bytes = b''
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("helvetica", size=12)
            safe_data = current_data.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=safe_data)
            pdf_bytes = pdf.output()
        except:
            pass
        st.download_button("📕 PDF", bytes(pdf_bytes), "extraction.pdf", "application/pdf", use_container_width=True)
    with col5:
        if st.button("🗑️ Discard", type="secondary", use_container_width=True):
            st.session_state['extracted_text'] = ""
            st.rerun()