"""Module for adding text annotations to PDF files."""
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


def add_text_annotation(input_pdf_path, output_pdf_path, text, x=100, y=750):
    """
    Add text annotation to the first page of a PDF.
    
    Args:
        input_pdf_path: Path to the input PDF file
        output_pdf_path: Path to save the annotated PDF file
        text: The text to add as annotation
        x: X coordinate for text position (default: 100)
        y: Y coordinate for text position (default: 750)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read the existing PDF
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()
        
        # Create a new PDF with the text annotation
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(x, y, text)
        can.save()
        
        # Move to the beginning of the BytesIO buffer
        packet.seek(0)
        
        # Read the annotation PDF
        annotation_pdf = PdfReader(packet)
        
        # Get the first page from the original PDF
        first_page = reader.pages[0]
        
        # Merge the annotation onto the first page
        first_page.merge_page(annotation_pdf.pages[0])
        
        # Add the modified first page to the writer
        writer.add_page(first_page)
        
        # Add all remaining pages unchanged
        for page_num in range(1, len(reader.pages)):
            writer.add_page(reader.pages[page_num])
        
        # Write the output PDF
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        print(f"Error adding text annotation: {e}")
        return False


def add_text_annotations_to_multiple_pdfs(pdf_files, output_dir, text, x=100, y=750):
    """
    Add text annotation to the first page of multiple PDF files.
    
    Args:
        pdf_files: List of paths to input PDF files
        output_dir: Directory to save the annotated PDF files
        text: The text to add as annotation
        x: X coordinate for text position (default: 100)
        y: Y coordinate for text position (default: 750)
    
    Returns:
        List of output file paths that were successfully annotated
    """
    import os
    
    success_files = []
    for pdf_path in pdf_files:
        basename = os.path.basename(pdf_path)
        output_path = os.path.join(output_dir, f"annotated_{basename}")
        
        if add_text_annotation(pdf_path, output_path, text, x, y):
            success_files.append(output_path)
    
    return success_files
