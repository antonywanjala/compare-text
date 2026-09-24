import os
import tempfile
from docx import Document
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def extract_text_from_docx(docx_path):
    """Extracts plain text paragraphs from a .docx file."""
    doc = Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())
    return "\n".join(full_text)


def extract_text_from_pdf(pdf_path):
    """Extracts plain text from all pages of a .pdf file."""
    reader = PdfReader(pdf_path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text and text.strip():
            full_text.append(text.strip())
    return "\n".join(full_text)


def convert_txt_to_pdf(text_content, output_pdf_path):
    """Generates a styled PDF from plain text using ReportLab."""
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    heading_style = styles['Heading2']

    # Custom paragraph style to preserve spacing
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=normal_style,
        fontSize=10,
        leading=14,
        spaceAfter=6
    )

    story = []

    # Parse plain text into ReportLab Flowables
    lines = text_content.splitlines()
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            story.append(Spacer(1, 8))
            continue

        if cleaned_line.startswith("===") and cleaned_line.endswith("==="):
            # Section separators / Header lines
            story.append(Spacer(1, 12))
            story.append(Paragraph(cleaned_line.replace("<", "&lt;").replace(">", "&gt;"), heading_style))
            story.append(Spacer(1, 6))
        else:
            # Standard text paragraph
            safe_text = cleaned_line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe_text, body_style))

    doc.build(story)


def process_and_merge_documents(input_directory, output_txt_path, output_pdf_path):
    """Loops through input files, extracts & merges text, saves TXT, and generates PDF."""

    # Filter valid docx and pdf files (ignoring hidden files like ._file.docx)
    files = sorted([
        f for f in os.listdir(input_directory)
        if not f.startswith('.') and (f.lower().endswith('.docx') or f.lower().endswith('.pdf'))
    ])

    merged_text_sections = []
    print(f"Processing {len(files)} document(s) in: {input_directory}\n" + "-" * 50)

    for filename in files:
        filepath = os.path.join(input_directory, filename)

        # Skip output target files if placed inside the input folder
        if os.path.abspath(filepath) in (os.path.abspath(output_txt_path), os.path.abspath(output_pdf_path)):
            continue

        print(f"[*] Extracting text from: {filename}")
        extracted_text = ""

        try:
            if filename.lower().endswith('.docx'):
                extracted_text = extract_text_from_docx(filepath)
            elif filename.lower().endswith('.pdf'):
                extracted_text = extract_text_from_pdf(filepath)

            if extracted_text.strip():
                header = f"=== SOURCE DOCUMENT: {filename} ==="
                merged_text_sections.append(f"{header}\n\n{extracted_text}\n")
                print(f"    -> Extracted {len(extracted_text)} characters.")
            else:
                print(f"    [!] Warning: No readable text found in {filename}.")

        except Exception as e:
            print(f"    [!] Error extracting from {filename}: {e}")

    # Combine all extracted sections
    full_merged_text = "\n\n".join(merged_text_sections)

    # 1. Save merged TXT
    print("-" * 50)
    print(f"Writing merged text file...")
    with open(output_txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(full_merged_text)
    print(f" -> Saved TXT to: {output_txt_path}")

    # 2. Build output PDF
    print(f"Generating PDF report from extracted text...")
    convert_txt_to_pdf(full_merged_text, output_pdf_path)
    print(f" -> Saved PDF to: {output_pdf_path}")

    print("\nSUCCESS: All documents processed, merged to TXT, and compiled to PDF!")


if __name__ == "__main__":
    target_folder = '/Users/antonywanjala/Downloads/Accounts 4'
    merged_txt_out = "/Users/antonywanjala/Downloads/Accounts 4/Merged_Output.txt"
    merged_pdf_out = "/Users/antonywanjala/Downloads/Accounts 4/Merged_Output.pdf"

    if not os.path.exists(target_folder):
        print("Error: Target directory does not exist.")
    else:
        process_and_merge_documents(target_folder, merged_txt_out, merged_pdf_out)
