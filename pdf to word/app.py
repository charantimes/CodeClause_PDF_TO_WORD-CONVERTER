from flask import Flask, request, render_template, send_file
from pdf2docx import parse
import os

app = Flask(__name__)
app.config['UPLOADER_FOLDER'] = ''

def convert_pdf2docx(input_file: str, output_file: str, pages=None):
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]

    result = parse(pdf_file=input_file, docx_with_path=output_file, pages=pages)
    summary = {
        "File": input_file,
        "Pages": str(pages),
        "Output File": output_file
    }
    print("\n".join("{}: {}".format(i, j) for i, j in summary.items()))
    return result

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        file = request.files['filename']
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOADER_FOLDER'], file.filename))
            input_file = file.filename
            output_file = "hello.docx"
            convert_pdf2docx(input_file, output_file)
            doc = input_file.split(".")[0] + ".docx"
            doc = doc.replace(" ", "=")
            return render_template("docx.html", variable=doc)
    return render_template("index.html")

@app.route('/docx', methods=['GET', 'POST'])
def docx():
    if request.method == "POST":
        filename = request.form.get('filename', None)
        filename = filename.replace("=", " ")
        return send_file(filename, as_attachment=True)
    return render_template("index.html")
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method=="POST":
        return render_template("index.html") 
if __name__ == "__main__":
    app.debug = True
    app.run()
