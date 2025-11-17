from flask import Flask, jsonify, request, send_file
import os
import tempfile
from pdf_annotator import add_text_annotation, add_text_annotations_to_multiple_pdfs

app = Flask(__name__)

balance = 0

@app.route('/')
def index():
    return jsonify({'balance': balance})

@app.route('/deposit')
def deposit():
    global balance
    amount = request.args.get('amount')
    balance = balance + int(amount)
    return jsonify({'balance': balance})

@app.route('/withdraw')
def withdraw():
    global balance
    amount = request.args.get('amount')
    if(int(amount) > balance):
        return jsonify({'balance': balance})    
    balance = balance - int(amount)
    return jsonify({'balance': balance})

@app.route('/annotate-pdf', methods=['POST'])
def annotate_pdf():
    """
    Endpoint to annotate a PDF file with text.
    Expects a file upload and 'text' parameter.
    Returns the annotated PDF.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    text = request.form.get('text', 'Annotated')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'File must be a PDF'}), 400
    
    # Create temporary files for input and output
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_input:
        file.save(tmp_input.name)
        input_path = tmp_input.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_output:
        output_path = tmp_output.name
    
    try:
        # Add annotation
        success = add_text_annotation(input_path, output_path, text)
        
        if not success:
            return jsonify({'error': 'Failed to annotate PDF'}), 500
        
        # Send the annotated file
        return send_file(output_path, 
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name=f'annotated_{file.filename}')
    finally:
        # Clean up temporary files
        if os.path.exists(input_path):
            os.unlink(input_path)
        # Note: output_path cleanup happens after send_file completes

if __name__ == '__main__':
    app.run(debug=True)
