import os
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask import session
from simplekv.memory import DictStore
from flaskext.kvsession import KVSessionExtension
import Student
import AeriesAPI

store = DictStore()
app = Flask(__name__)
Flask.secret_key='Develop'

KVSessionExtension(store, app)

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
	if request.method=='POST':
		user=request.form['user']
		pw=request.form['pass']
		try:
			student=Student.Student(user,pw)
		except Exception as e:
			return render_template('login.html', error=True)

		session["user"]=user
		session["pw"]=pw
		return render_template('gradebook.html', user=user, pw=pw, periods=student.periods)

@app.route('/class/<class_id>')
def period(class_id):
	assignments=[]
	student=Student.Student(session["user"],session["pw"])
	for period in student.periods:
		if(period["class_id"]==class_id):
			period_name=period["name"]
	period_stuff=student.aeries.getPeriodAssignments(class_id)
	assignments= period_stuff['assignments']
	total_scores=period_stuff['totalscores']
	weighted=period_stuff['weighted']
	assignment_types=[]
	for assignment in assignments:
		ass_type= assignment["type"]
		if ass_type not in assignment_types:
			assignment_types.append(ass_type)
	new_ass= []
	for ass_type in assignment_types:
		new_ass.append({
			"type": ass_type,
			"assignments": [ass for ass in assignments if ass["type"]==ass_type]
		})
	assignments=new_ass
	return render_template('class.html', assignments=assignments, total_scores= total_scores, period_name=period_name, weighted=weighted)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)