import connexion
import datetime
import logging
from os import getenv
import jobber_orm as jorm
import jobber_api_utils as jau

db_session = None


def get_questions():
    """
    Get a list of questions.

    :return: questions
    :rtype: dict
    """
    logging.info("get_questions endpoint called")

    db_response = db_session.query(jorm.Question)

    if db_response is None:
        response_info = jau.create_return_object()
    else:
        response_data = dict()
        response_data['questions'] = list()
        for question in db_response:
            response_data['questions'].append(question.dump())

        response_info = jau.create_return_object(data=response_data)

    return response_info, 200


def get_question(question_id):
    """
    Get a single question.

    :param question_id: ID of the question
    :return: a single question
    :rtype: dict
    """
    logging.info("get_question endpoint called")

    db_response = db_session.query(jorm.Question).filter(jorm.Question.id == question_id).one_or_none()

    if db_response is None:
        error_response = jau.create_return_object(error_status=True,
                                                  error_message="Not Found")
        return error_response, 404
    else:
        response_data = db_response.dump()
        response_info = jau.create_return_object(data = response_data)
        return response_info, 200


def put_question(question_id, question):
    """
    Create or update a question.

    :param str question_id: the id of the question
    :param dict question: the question to update or save
    :return: result of the question submission
    :rtype: dict
    """
    logging.info("put_question endpoint called")

    db_response = db_session.query(jorm.Question).filter(jorm.Question.id == question_id).one_or_none()
    question['id'] = question_id

    if db_response is not None:
        logging.info("Updating question {}".format(question_id))
        db_response.update(**question)
        response = jau.create_return_object()
    else:
        logging.info("Creating question {}".format(question_id))
        question['created_at'] = datetime.datetime.utcnow()
        question['updated_at'] = datetime.datetime.utcnow()
        db_session.add(jorm.Question(**question))
        response = jau.create_return_object()

    db_session.commit()

    return response, (200 if question is not None else 201)


def delete_question(question_id):
    """
    Delete a question

    :param int question_id: ID of the question
    :return: HTTP status code
    """
    logging.info("delete_question endpoint called")

    question = db_session.query(jorm.Question).filter(jorm.Question.id == question_id).one_or_none()

    if question is not None:
        logging.info('Deleting question {}', question_id)
        db_session.query(jorm.Question).filter(jorm.Question.id == question_id).delete()
        db_session.commit()
        response = jau.create_return_object()
        return response, 200
    else:
        response = jau.create_return_object(error_status=True,
                                            error_message="Not Found")
        return response, 404


def get_job_applications():
    """
    Get a list of accepted job applications

    :return: approved job applications
    :rtype: dict
    """
    logging.info("get_job_applications endpoint called")

    db_response = db_session.query(jorm.JobApplication)

    if db_response is None:
        response_info = jau.create_return_object()
    else:
        response_data = dict()
        response_data['job_applications'] = list()
        for job_application in db_response:
            response_data['job_applications'].append(job_application.dump())

        response_info = jau.create_return_object(data=response_data)

    return response_info, 200


def get_job_application(job_application_id):
    """
    Get a single job application

    :param int job_application_id: ID of the job application
    :return: job application information
    :rtype: dict
    """
    logging.info("get_job_application endpoint called")

    db_response = db_session.query(jorm.JobApplication).filter(jorm.JobApplication.id == job_application_id).one_or_none()

    if db_response is None:
        error_response = jau.create_return_object(error_status=True,
                                                  error_message="Not Found")
        return error_response, 404
    else:
        response_data = db_response.dump()
        response_info = jau.create_return_object(data=response_data)
        return response_info, 200


def put_job_application(job_application_id, job_application):
    """
    Validate and save a job application.

    :param str job_application_id: the id of the job application
    :param dict job_application: the job application
    :return: result of the application: accepted or rejected
    :rtype: dict
    """
    logging.info("put_job_application endpoint called")

    db_response = db_session.query(jorm.JobApplication).filter(jorm.JobApplication.id == job_application_id).one_or_none()
    job_application['id'] = job_application_id

    if db_response is not None:
        logging.info("Updating job application {}".format(job_application_id))
        db_response.update(**job_application)
        response = jau.create_return_object()
    else:
        logging.info("Creating job application {}".format(job_application_id))
        job_application['created_at'] = datetime.datetime.utcnow()
        job_application['updated_at'] = datetime.datetime.utcnow()
        db_session.add(jorm.JobApplication(**job_application))
        response = jau.create_return_object()

    db_session.commit()

    return response, (200 if job_application is not None else 201)


def delete_job_application(job_application_id):
    """
    Delete a job application.

    :param int job_application_id: ID of the job application
    :return: HTTP status code
    """
    logging.info("delete_job_application endpoint called")

    db_response = db_session.query(jorm.JobApplication).filter(jorm.JobApplication.id == job_application_id).one_or_none()

    if db_response is not None:
        logging.info('Deleting job application {}', job_application_id)
        db_session.query(jorm.JobApplication).filter(jorm.JobApplication.id == job_application_id).delete()
        db_session.commit()
        response = jau.create_return_object()
        return response, 200
    else:
        response = jau.create_return_object(error_status=True,
                                            error_message="Not Found")
        return response, 404


logging.basicConfig(level=logging.INFO)
db_session = jorm.init_db('sqlite:///:memory:')
app_port = int(getenv('API_PORT', 8080))

app = connexion.FlaskApp(__name__,
                        specification_dir='.',
                        server='tornado')

app.add_api('jobber_api.yaml',
            strict_validation=True,
            swagger_json=True)

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def run_server():
    # Run Jobber
    app.run(port=app_port)

if __name__ == '__main__':
    run_server()
