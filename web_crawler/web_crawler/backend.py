from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    # Run the Scrapy spider with the provided search term
    os.system(f'scrapy crawl manuals -a search_term="{search_term}"')
    # Redirect to the page listing the downloaded PDFs
    return redirect(url_for('pdf_list'))
@app.route('/pdf_list')
def pdf_list():
    directory = '/Users/zackchand/Downloads/pdfs/'
    pdf_files = [file for file in os.listdir(directory) if file.endswith(".pdf")]
    return render_template('pdf_list.html', pdf_files=pdf_files)

@app.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    """
    Route to serve PDF files.
    """
    directory = '/Users/zackchand/Downloads/pdfs/'
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True)
