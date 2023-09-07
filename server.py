import os
import numpy as np
import flask
from flask import Flask, request, jsonify,  render_template
import pickle

app = Flask(__name__)

model = pickle.load(open('customer_churn_model.pkl','rb'))

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():

    return flask.render_template('index.html')


# get data from the html form and perform prediction
@app.route('/result',methods = ['POST'])
def result():
	if request.method == 'POST':
		cid = request.form['CustomerID']
		name = request.form['Name']
		age = int(request.form['Age'])
		gen = request.form['Gender']
		loc = request.form['Location']
		slm = int(request.form['Subscription_Length_Months'])
		mb = float(request.form['Monthly_Bill'])
		tugb = float(request.form['Total_Usage_GB'])

		#convert str to int
		if loc =='Houston':
			new_loc=1
		elif loc=='Los Angeles':
			new_loc=2
		elif loc=='Miami':
			new_loc=3
		elif loc=='Chicago':
			new_loc=4
		elif loc=='New York':
			new_loc=5
		else:
			print('Not found')
		#convert str to int
		if gen=='Male':
			new_gen=1
		elif gen=='Female':
			new_gen=0
		else:
			print('Not found')
		
		input = [age, new_gen, new_loc, slm, mb, tugb]

		prediction = model.predict([input])
		output = prediction[0]
		
		if (output == 0):
			out= 'Customer '+ cid +':not churn'
		else:
			out= 'Customer '+ cid + ':churn'

		return render_template("result.html", prediction=out)


if __name__ == '__main__':
	app.run(port=5000, debug=True)
