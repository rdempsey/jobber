from datetime import datetime
import requests
from os import getenv
import logging
from flask import Flask, abort, flash, redirect, render_template, request, url_for
import traceback
from momentjs import momentjs
import uuid

app = Flask(__name__)
app.jinja_env.globals['momentjs'] = momentjs
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'

app_port = int(getenv('APP_PORT', '5000'))
questions_endpoint = getenv('QUESTIONS_ENDPOINT', 'http://localhost:8080/1.0/questions')
application_endpoint = getenv('APPLICATION_ENDPOINT', 'http://localhost:8080/1.0/job-applications')


@app.route('/')
def show_home_page():
    return render_template('dashboard.html')


@app.route('/job-applications', methods = ['GET'])
def show_job_applications():
    job_applications = list()

    r = requests.get(application_endpoint)
    response = r.json()

    for job_application in response['data']['job_applications']:
        # Datetime format: 2017-04-08 18:33:43.303353
        job_application['created_at'] = datetime.strptime(job_application['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        job_application['updated_at'] = datetime.strptime(job_application['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        logging.info(job_application)
        job_applications.append(job_application)

    sorted_applications = sorted(job_applications, key=lambda k: k['created_at'], reverse=True)

    return render_template('job_applications/list.html', job_applications=sorted_applications)


@app.route('/job-applications/<job_application_id>', methods = ['GET'])
def show_job_application(job_application_id):
    url = "{}/{}".format(application_endpoint, job_application_id)
    r = requests.get(url)
    response = r.json()

    job_application = response['data']
    job_application['created_at'] = datetime.strptime(job_application['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    job_application['updated_at'] = datetime.strptime(job_application['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

    return render_template('job_applications/show.html', job_application=job_application)


@app.route('/questions', methods = ['GET', 'POST'])
def show_questions():

    if request.method == 'POST':
        qid = uuid.uuid5(uuid.NAMESPACE_DNS, 'jobber')      # application name
        qid = uuid.uuid5(qid, request.form['question'])     # question
        qid = uuid.uuid5(qid, request.form['answer'])       # answer

        question_data = {
            "id": str(qid),
            "question": request.form['question'],
            "answer": request.form['answer']
        }
        url = "{}/{}".format(questions_endpoint, question_data['id'])
        requests.put(url, json=question_data)


    questions = list()

    r = requests.get(questions_endpoint)
    response = r.json()

    for question in response['data']['questions']:
        question['created_at'] = datetime.strptime(question['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        question['updated_at'] = datetime.strptime(question['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        questions.append(question)

    sorted_questions = sorted(questions, key=lambda k: k['id'], reverse=False)

    return render_template('questions/list.html', questions=sorted_questions)


@app.route('/questions/<question_id>', methods = ['POST'])
def update_question(question_id):
    try:
        question_data = {
            "id": question_id,
            "question": request.form['question'],
            "answer": request.form['answer']
        }
        url = "{}/{}".format(questions_endpoint, question_data['id'])
        requests.put(url, json=question_data)
    except:
        logging.error(traceback.format_exc())

    return redirect('questions')


@app.route('/questions/<question_id>', methods = ['GET'])
def edit_question(question_id):
    url = "{}/{}".format(questions_endpoint, question_id)
    r = requests.get(url)
    response = r.json()
    return render_template('questions/edit.html', question=response['data'])


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_port)