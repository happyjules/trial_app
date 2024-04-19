import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import os 



def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['xlsx', 'xls']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def aggregate_deductible(filename):
    df = pd.read_excel(filename)
    aggregated_data = df[['Patient', 'Ded']].groupby('Patient').sum()
    aggregated_data.reset_index(inplace=True)
    return aggregated_data


app = Flask(__name__)
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
        result_df = aggregate_deductible(file.filename)
        return render_template('result.html', tables=[result_df.to_html(index=False)])
    else:
        return render_template('error.html')


if __name__ == '__main__':
    app.run()
