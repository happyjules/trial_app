import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import sys, os

MAX_CONTENT_LENGTH = 1024 * 1024 *5
UPLOAD_FOLDER = "uploads"
def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['xlsx', 'xls']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_config_dir():
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    template_dir = os.path.join(datadir, 'templates')
    static_dir = os.path.join(datadir, "static")
    return template_dir, static_dir
    
template_dir, static_dir = get_config_dir()    
app = Flask(__name__, 
            template_folder=template_dir, 
            static_folder=static_dir)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.route("/")
def home():
    return render_template('index.html')
  
  
@app.route('/help')
def help():
    return 'slack @julie'


@app.route('/result', methods=['POST'])
def upload_file():
    # Check if a file is uploaded
    if 'excel' not in request.files:
        return redirect(request.url)
    file = request.files['excel']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.save(file.filename)
        df = pd.read_excel(file.filename)
        if 'Patient' in df.columns and 'Ded' in df.columns:
            aggregated_data = df[['Patient', 'Ded']].groupby('Patient').sum()
            aggregated_data.reset_index(inplace=True)
            return render_template('result.html', tables=[aggregated_data.to_html(index=False)])
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(port=3000)
