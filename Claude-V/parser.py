"""
Parser Agent — extracts text from downloaded PDFs using PyMuPDF (fitz).
"""
import os
import glob

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file using PyMuPDF.
    Returns the full text as a string.
    Falls back gracefully if the file can't be opened.
    """
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
    except ImportError:
        print("[ParserAgent] PyMuPDF not installed. Install with: pip install PyMuPDF")
        return _fallback_text_extraction(pdf_path)
    except Exception as e:
        print(f"[ParserAgent] Cannot open {pdf_path}: {e}")
        return ""

    text_parts = []
    for page_num, page in enumerate(doc):
        try:
            page_text = page.get_text("text")  # plain text
            if page_text.strip():
                text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
        except Exception as e:
            print(f"[ParserAgent] Error on page {page_num + 1}: {e}")
            continue

    doc.close()
    return "\n".join(text_parts)


def _fallback_text_extraction(pdf_path: str) -> str:
    """Fallback: try pdfplumber if PyMuPDF unavailable."""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )
    except Exception as e:
        print(f"[ParserAgent] Fallback extraction also failed: {e}")
        return ""


def process_all_pdfs(folder: str = "data/raw_docs", output_folder: str = "data/text"):
    """
    Batch-process all PDFs in a folder. Saves .txt files in output_folder.
    Returns dict of {filename: extracted_text}.
    """
    os.makedirs(output_folder, exist_ok=True)
    results = {}
    for pdf_path in glob.glob(os.path.join(folder, "*.pdf")):
        text = extract_text_from_pdf(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        out_path = os.path.join(output_folder, base_name + ".txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        results[base_name] = text
        print(f"[ParserAgent] Processed {pdf_path} → {out_path} ({len(text)} chars)")
    return results
