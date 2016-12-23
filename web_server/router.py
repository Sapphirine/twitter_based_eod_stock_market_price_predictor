#
# Start a server
# 
# index page to welcome user and allow user enter company name and text
# 
# return page show the graph of data and render other components
#
from __future__ import print_function
from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import os.path



import pandas as pd
import numpy as np
import flask
from pandas import *
import requests
import sys
import dill

app = Flask(__name__)
app.vars={}
Company_list = ['AAPL', 'MSFT', 'VZ', 'T', 'WMT', 'AMZN', 'DIS', 'NFLX']

def init_csv(Company_list):
	for company in Company_list:
		if os.path.exists('%s.csv' % company):
			continue
		else:
			API_url='https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?api_key=a5-JLQBhNfxLnwxfXoUE' % company
			pd.read_csv(API_url, parse_dates=['Date']).to_csv('%s.csv' % company)

init_csv(Company_list)
print ("all_data_get", file=sys.stderr)

def load_models(Company_Name,Twitter_text):

    if Company_Name == 'AAPL':
        return dill.load(open('static/models/apple.pkl',"r")).predict([Twitter_text])
    elif Company_Name == 'MSFT':
        return dill.load(open('static/models/microsoft.pkl',"r")).predict([Twitter_text])
    elif Company_Name == 'VZ':
        return dill.load(open('static/models/verizon.pkl',"r")).predict([Twitter_text])
    elif Company_Name == 'T':
        return dill.load(open('static/models/att.pkl',"r")).predict([Twitter_text])
    elif Company_Name == 'WMT':
        return dill.load(open('static/models/walmart.pkl',"r")).predict([Twitter_text])
    elif Company_Name == 'AMZN':
        return dill.load(open('static/models/amazon.pkl',"r")).predict([Twitter_text])
    elif Company_Name == 'DIS':
        return dill.load(open('static/models/disney.pkl',"r")).predict([Twitter_text])
    elif Company_Name == 'NFLX':
        return dill.load(open('static/models/netflix.pkl',"r")).predict([Twitter_text])
    else:
        return redirect('/error.html')

def get_company_histogram(Company_Name, Twitter_text):
    #API_url='https://www.quandl.com/api/v3/datasets/WIKI/%s.csv?api_key=a5-JLQBhNfxLnwxfXoUE' % Company_Name
    #r = requests.get(API_url)
    #if r.status_code == 404:
    #    return render_template('error.html')
    if Company_Name not in Company_list:
        return redirect('/error.html')
    data = pd.read_csv('%s.csv' % Company_Name, parse_dates=['Date'])
    Colors=["blue","green","yellow","red"]
    Color_index=0
    target_data=data.ix[:,['Open','Adj. Open','Close','Adj. Close']]
    p=figure(x_axis_type="datetime", title='Data from Quandle WIKI set')
    p.xaxis.axis_label = 'Date'
    if 'Close' in app.vars['features']:
        p.line(x=data['Date'],y=target_data['Close'],legend="%s:Close" % Company_Name, line_color=Colors[Color_index])
        Color_index = Color_index +1
    if 'Adj. Close' in app.vars['features']:
        p.line(x=data['Date'],y=target_data['Adj. Close'],legend="%s:Adj. Close" % Company_Name, line_color=Colors[Color_index])
        Color_index = Color_index +1
    if 'Open' in app.vars['features']:
        p.line(x=data['Date'],y=target_data['Open'],legend="%s:Open" % Company_Name, line_color=Colors[Color_index])
        Color_index = Color_index +1
    if 'Adj. Open' in app.vars['features']:
        p.line(x=data['Date'],y=target_data['Adj. Open'],legend="%s:Adj. Open" % Company_Name, line_color=Colors[Color_index])

    #get company status
    predict_value = load_models(Company_Name,Twitter_text)

    if predict_value[0] > 0.5:
    	stock_status = "Good"
    else:
    	stock_status = "Bad"

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script, div = components(p, INLINE)
    logo_path = "/static/%s.png" % Company_Name
    good_or_bad = "/static/%s.jpg" % stock_status
    html = flask.render_template(
        'embed.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        Company_Name= Company_Name,
        Twitter_text= Twitter_text,
        logo_path= logo_path,
        good_or_bad= good_or_bad
    )
    return html


@app.route('/')
def main():
    return redirect('/welcome')

@app.route('/welcome', methods=['GET', 'POST'])
def get_welcome_data():
	if request.method == 'GET':
		return render_template('welcome.html')
	else:
		#Get information from front end
		print('Hello world!', file=sys.stderr)
		app.vars['Company_Name'] = request.form['stock_name']
		app.vars['Twitter_text'] = request.form['Twitter_text']
		app.vars['features'] = ['Open','Close']

		print (app.vars['Company_Name'], file=sys.stderr)
		print (app.vars['Twitter_text'], file=sys.stderr)
		html = get_company_histogram(app.vars['Company_Name'],app.vars['Twitter_text'])
		#
		return encode_utf8(html)

if __name__ == '__main__':
  app.run(port=33507, debug=True)