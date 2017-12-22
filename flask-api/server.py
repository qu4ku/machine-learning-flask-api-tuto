import os
import pandas as pd
from sklearn.externals import joblib
from flask import Flask, jsonify, request
import dill as pickle

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def apicall():
	"""API Call
	Pandas dataframe (sent as payload) from API Call
	"""
	try:
		test_json = request.get_json()
		test = pd.read_json(test_json, orient='records')

		# To resolve the issue of TypeError: CAnnot compare types 
		# 'ndarray(dtype=int64)' and 'str'
		test['Dependents'] = [str(x) for x in list(test['Dependents'])]

		# Getting the Load_IDs separated out
		loan_ids = test['Loan_ID']

	except Exception as e:
		raise e

	clf = 'model_v2.pk'

	if test.empty:
		return(bad_request())
	else:
		# Load the saved model
		print('Loading the model...')
		loaded_model = None
		with open('./models/' + clf, 'rb') as f:
			print(f)
			loaded_model = pickle.load(f)

		print('The model has been loaded... doing predicions now...')
		predictions = loaded_model.predict(test)

		"""Add the predictions as Series to a new pandas dataframe
		OR Depending on the use-case, the entire test data appended with the new files
		"""

		prediction_series = list(pd.Series(predictions))

		final_predictions = pd.DataFrame(list(zip(loan_ids, prediction_series)))

		"""We can be as creative in sending the responses.
		   But we need to send the response codes as well.
		"""
		resp = jsonify(predictions=final_predictions.to_json(orient='records'))
		resp.status_code = 200

		return resp


@app.errorhandler(400)
def bad_request(error=None):
	message = {
		'status': 400,
		'message': 'Bad Request: ' + request.url + '--> Please check your data payload...',
	}
	resp = jsonify(message)
	resp.status_code = 400
