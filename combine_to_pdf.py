import os
from pathlib import Path
from docx2pdf import convert
from pypdf import PdfWriter  # <-- Updated this import
from docx import Document
from docxcompose.composer import Composer


def combine_to_docx(docx_files, output_path):
    print(f"\nMerging {len(docx_files)} files into one DOCX...")

    # Set the first document as the master template
    master = Document(docx_files[0])
    composer = Composer(master)

    # Append the rest of the documents
    for file in docx_files[1:]:
        print(f"Appending: {file.name}")
        doc = Document(file)
        # Adding a page break before appending ensures each doc starts on a new page
        master.add_page_break()
        composer.append(doc)

    composer.save(output_path)
    print(f"Success! Merged DOCX saved to: {output_path}")


def combine_to_pdf(input_folder, docx_files, output_path):
    print("\nConverting DOCX files to PDF. This may take a moment...")

    # Convert all files in the input folder to PDF in-place
    convert(str(input_folder))

    # Collect the expected PDF paths based on the DOCX file names
    pdf_files = [f.with_suffix('.pdf') for f in docx_files]

    # <-- Use PdfWriter instead of PdfMerger
    merger = PdfWriter()

    print("Merging PDFs...")
    for pdf in pdf_files:
        if pdf.exists():
            print(f"Appending: {pdf.name}")
            merger.append(pdf)

    merger.write(output_path)
    merger.close()

    # Clean up the individual PDFs from the input folder to avoid clutter
    for pdf in pdf_files:
        if pdf.exists():
            pdf.unlink()

    print(f"Success! Merged PDF saved to: {output_path}")


def main():
    print("=== Document Merger Utility ===")
    input_dir = input("Enter the path to the input folder (containing DOCX files): ").strip()

    # Strip quotes in case the user dragged-and-dropped the folder into the terminal
    input_folder = Path(input_dir.strip('"').strip("'"))

    if not input_folder.is_dir():
        print(f"Error: The input directory '{input_folder}' does not exist.")
        return

    docx_files = sorted(input_folder.glob("*.docx"))

    if not docx_files:
        print("No .docx files found in the specified input folder.")
        return

    output_dir = input("Enter the path to the output folder: ").strip()
    output_folder = Path(output_dir.strip('"').strip("'"))

    # Create the output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    choice = input("Enter output format (pdf, docx, or both): ").strip().lower()

    if choice in ['docx', 'both']:
        docx_output = output_folder / "Merged_Document.docx"
        combine_to_docx(docx_files, docx_output)

    if choice in ['pdf', 'both']:
        pdf_output = output_folder / "Merged_Document.pdf"
        combine_to_pdf(input_folder, docx_files, pdf_output)

    if choice not in ['pdf', 'docx', 'both']:
        print("Invalid choice. Please run the script again and select 'pdf', 'docx', or 'both'.")


if __name__ == "__main__":
    main()
