"""Tests for PDF annotation functionality."""
import pytest
import os
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import shutil

from pdf_annotator import add_text_annotation, add_text_annotations_to_multiple_pdfs


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_pdf(temp_dir):
    """Create a sample PDF for testing."""
    pdf_path = os.path.join(temp_dir, 'test.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 700, "Original content")
    c.showPage()
    c.drawString(100, 700, "Second page")
    c.save()
    return pdf_path


@pytest.fixture
def sample_single_page_pdf(temp_dir):
    """Create a single page sample PDF for testing."""
    pdf_path = os.path.join(temp_dir, 'single_page.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 700, "Single page content")
    c.save()
    return pdf_path


def test_add_text_annotation_success(sample_pdf, temp_dir):
    """Test successfully adding text annotation to PDF."""
    output_path = os.path.join(temp_dir, 'annotated.pdf')
    text = "Test Annotation"
    
    result = add_text_annotation(sample_pdf, output_path, text)
    
    assert result is True
    assert os.path.exists(output_path)
    
    # Verify the output PDF has the same number of pages
    original_reader = PdfReader(sample_pdf)
    annotated_reader = PdfReader(output_path)
    assert len(annotated_reader.pages) == len(original_reader.pages)


def test_add_text_annotation_single_page(sample_single_page_pdf, temp_dir):
    """Test adding text annotation to single page PDF."""
    output_path = os.path.join(temp_dir, 'annotated_single.pdf')
    text = "Single Page Annotation"
    
    result = add_text_annotation(sample_single_page_pdf, output_path, text)
    
    assert result is True
    assert os.path.exists(output_path)
    
    # Verify the output PDF has 1 page
    annotated_reader = PdfReader(output_path)
    assert len(annotated_reader.pages) == 1


def test_add_text_annotation_custom_position(sample_pdf, temp_dir):
    """Test adding text annotation at custom position."""
    output_path = os.path.join(temp_dir, 'annotated_custom.pdf')
    text = "Custom Position"
    x, y = 200, 500
    
    result = add_text_annotation(sample_pdf, output_path, text, x, y)
    
    assert result is True
    assert os.path.exists(output_path)


def test_add_text_annotation_invalid_input():
    """Test handling of invalid input file."""
    result = add_text_annotation('nonexistent.pdf', 'output.pdf', 'text')
    assert result is False


def test_add_text_annotations_to_multiple_pdfs(temp_dir):
    """Test adding annotations to multiple PDF files."""
    # Create multiple test PDFs
    pdf_files = []
    for i in range(3):
        pdf_path = os.path.join(temp_dir, f'test{i}.pdf')
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 700, f"PDF {i}")
        c.save()
        pdf_files.append(pdf_path)
    
    output_dir = os.path.join(temp_dir, 'output')
    os.makedirs(output_dir)
    text = "Batch Annotation"
    
    result = add_text_annotations_to_multiple_pdfs(pdf_files, output_dir, text)
    
    assert len(result) == 3
    for output_path in result:
        assert os.path.exists(output_path)
        assert 'annotated_' in os.path.basename(output_path)


def test_add_text_annotations_empty_list(temp_dir):
    """Test handling of empty PDF list."""
    output_dir = os.path.join(temp_dir, 'output')
    os.makedirs(output_dir)
    
    result = add_text_annotations_to_multiple_pdfs([], output_dir, "text")
    
    assert result == []


def test_add_text_annotations_mixed_valid_invalid(temp_dir):
    """Test batch annotation with mix of valid and invalid files."""
    # Create one valid PDF
    valid_pdf = os.path.join(temp_dir, 'valid.pdf')
    c = canvas.Canvas(valid_pdf, pagesize=letter)
    c.drawString(100, 700, "Valid PDF")
    c.save()
    
    pdf_files = [valid_pdf, 'nonexistent.pdf']
    output_dir = os.path.join(temp_dir, 'output')
    os.makedirs(output_dir)
    
    result = add_text_annotations_to_multiple_pdfs(pdf_files, output_dir, "text")
    
    # Should only succeed for the valid file
    assert len(result) == 1
    assert os.path.exists(result[0])
