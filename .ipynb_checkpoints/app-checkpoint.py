from flask import Flask, render_template

app = Flask(__name__)


import os
from data_functions import load_lines_from_raw, groupby_country, features, aggs
home = os.environ['HOME'] # this can go within the function
data_file = os.path.join(home, 'dkb-data', 'raw', 'cdn_20200117-20200123.log') #this can go within the function


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/report')
def reports():
    report_id = 'OriginResponseTime'
    data = loader_raw_lines(data_file, 50)
    report = data.loc[:, report_id]
    
    stats = {
        'min': report.min(), 'std': report.std(), 'max': report.max()
    }
    #img_fldr = os.path.join(home, 'dkb-data', 'reports', report_id)
    
    img_fldr = os.path.join('static', report_id)
    
    img = [i for i in os.listdir(img_fldr) if i[-4:] == '.png'] #important piece of code i[-4:] this shows the last 4
    img = [os.path.join(img_fldr, i) for i in img]
    img = [{'source': i} for i in img]
    
#     import pdb; pdb.set_trace() #This is a great debugger line and this tells you that you have an intermediate level in python
   
    
    #plot_gleb = create_target_report_gleb(data, report_id)
    
    return render_template('report.html', report_id =report_id, data=report.to_json(), stats=stats, img=img)


@app.route('/countries')
def countries():
    data = load_lines_from_raw(5000)
    grps = groupby_country(features, aggs, data)
    grps = grps.reset_index()
    return render_template('countries.html', countries=grps.to_dict(orient='records'))


@app.route('/data')
def raw_data():
    return loader_raw_lines(data_file, 50).to_json()


if __name__ == '__main__':
    app.run(debug=True)