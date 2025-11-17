# BankAccount
This is an educational public repository to illustrate the power of automated testing through Github Actions.

## Run locally
1. Set up Python virtual environment.
```
python -m venv venv
```
2. Install required dependencies.
```
pip install -r requirements.txt
```
3. Run unit tests.
```
python -m pytest
```
4. Run the app.
```
python app.py
```

## PDF Annotation Feature

The application now includes functionality to add text annotations to the first page of PDF files.

### Using the API Endpoint

You can use the `/annotate-pdf` endpoint to annotate PDFs:

```bash
curl -X POST http://localhost:5000/annotate-pdf \
  -F "file=@your-document.pdf" \
  -F "text=Your annotation text" \
  -o annotated-document.pdf
```

### Using the Python Module

You can also use the `pdf_annotator` module directly:

```python
from pdf_annotator import add_text_annotation, add_text_annotations_to_multiple_pdfs

# Annotate a single PDF
add_text_annotation('input.pdf', 'output.pdf', 'My Annotation', x=100, y=750)

# Annotate multiple PDFs
pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']
add_text_annotations_to_multiple_pdfs(pdf_files, './output_dir', 'Batch Annotation')
```

### Parameters

- `text`: The text to add as annotation (default: "Annotated")
- `x`: X coordinate for text position (default: 100)
- `y`: Y coordinate for text position (default: 750)

The annotation is added only to the first page of each PDF, while all other pages remain unchanged.

## Code Description

1. app.py: A flask application that exposes the following API endpoints: 
  - index at / : Retun a JSON data structure indicating the current balance. 
  - deposit at /deposit : Take the deposit amount as a URL parameter and return the new balance after adding the amount. 
  - withdraw at /withdraw : Take the withdrawal amount as a URL parameter and return the new balance after subtracting the amount.
  - annotate-pdf at /annotate-pdf : Accept a PDF file upload and add text annotation to its first page. Expects a POST request with 'file' (PDF file) and optional 'text' (annotation text) parameters.
App relies on a global in-memory variable (`balance`) to store the balance of the account.

2. pdf_annotator.py: A module for adding text annotations to PDF files. Contains functions for annotating single PDFs and batch processing multiple PDFs.

3. requirements.txt: A text file including all the Python libraries and packages needed to run the app. 

4. .gitignore: Refer to the gitignore article for more details. In short, this file makes it possible that local configuration or binary files are not pushed to the repository. 

5. tests: It's a directory that includes several unit tests for the APIs. The tests utilize the PyTest library.