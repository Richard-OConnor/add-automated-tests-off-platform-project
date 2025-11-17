import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import os

def test_balance(app, client):
    del app
    res = client.get('/')
    assert res.status_code == 200
    expected = {'balance': 0}
    assert expected == json.loads(res.get_data(as_text=True))

def test_deposit(app, client):
    del app
    res = client.get('/deposit?amount=500')
    assert res.status_code == 200
    expected = {'balance': 500}
    assert expected == json.loads(res.get_data(as_text=True))

def test_deposit_2(app, client):
    del app
    res = client.get('/deposit?amount=300')
    assert res.status_code == 200
    expected = {'balance': 800}
    assert expected == json.loads(res.get_data(as_text=True))

def test_withdraw_1(app, client):
    del app
    res = client.get('/withdraw?amount=1000')
    assert res.status_code == 200
    expected = {'balance': 800}
    assert expected == json.loads(res.get_data(as_text=True))

def test_withdraw_2(app, client):
    del app
    res = client.get('/withdraw?amount=100')
    assert res.status_code == 200
    expected = {'balance': 700}
    assert expected == json.loads(res.get_data(as_text=True))

def test_deposit_3(app, client):
    del app
    res = client.get('/deposit?amount=500')
    assert res.status_code == 200
    expected = {'balance': 1200}
    assert expected == json.loads(res.get_data(as_text=True))

def test_withdraw_3(app, client):
    del app
    res = client.get('/withdraw?amount=1000')
    assert res.status_code == 200
    expected = {'balance': 200}
    assert expected == json.loads(res.get_data(as_text=True))

def test_balance_2(app, client):
    del app
    res = client.get('/')
    assert res.status_code == 200
    expected = {'balance': 200}
    assert expected == json.loads(res.get_data(as_text=True))

def test_annotate_pdf_success(app, client):
    """Test PDF annotation endpoint with valid PDF."""
    del app
    
    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as tmp:
        c = canvas.Canvas(tmp.name, pagesize=letter)
        c.drawString(100, 700, "Test content")
        c.save()
        tmp_path = tmp.name
    
    try:
        # Upload the PDF
        with open(tmp_path, 'rb') as f:
            data = {
                'file': (f, 'test.pdf'),
                'text': 'Annotated Text'
            }
            res = client.post('/annotate-pdf', 
                            data=data,
                            content_type='multipart/form-data')
        
        assert res.status_code == 200
        assert res.content_type == 'application/pdf'
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def test_annotate_pdf_no_file(app, client):
    """Test PDF annotation endpoint without file."""
    del app
    res = client.post('/annotate-pdf', data={})
    assert res.status_code == 400
    data = json.loads(res.get_data(as_text=True))
    assert 'error' in data
    assert 'No file provided' in data['error']

def test_annotate_pdf_empty_filename(app, client):
    """Test PDF annotation endpoint with empty filename."""
    del app
    data = {
        'file': (b'', '')
    }
    res = client.post('/annotate-pdf', 
                     data=data,
                     content_type='multipart/form-data')
    assert res.status_code == 400
    data = json.loads(res.get_data(as_text=True))
    assert 'error' in data
    assert 'No file selected' in data['error']

def test_annotate_pdf_non_pdf_file(app, client):
    """Test PDF annotation endpoint with non-PDF file."""
    del app
    
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write('test content')
        tmp_path = tmp.name
    
    try:
        with open(tmp_path, 'rb') as f:
            data = {
                'file': (f, 'test.txt'),
                'text': 'Some text'
            }
            res = client.post('/annotate-pdf', 
                            data=data,
                            content_type='multipart/form-data')
        
        assert res.status_code == 400
        data = json.loads(res.get_data(as_text=True))
        assert 'error' in data
        assert 'must be a PDF' in data['error']
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)