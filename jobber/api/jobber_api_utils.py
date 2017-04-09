"""
jobber.api.jobber_api_utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Handy functions used by the Jobber API.

"""

from fuzzywuzzy import fuzz
from statistics import mean
from copy import deepcopy


def create_return_object(error_status=False, error_cause=None, error_message=None, data=None):
    """
    Create generic response objects.

    :param bool error_status: True if there is an error to report
    :param str error_cause: The cause of the error
    :param str error_message: The error message to return to the user
    :param dict data: Any additional data to return
    :returns: dict return_object A dictionary of containing a success or failure message and any additional data
    """

    return_object = {}

    if error_status:
        # Add the Pulse status
        return_object['status'] = 'FAILURE'
        # Add the error section with sub_code and message
        return_object['error'] = {}
        # Add the cause
        return_object['error']['cause'] = error_cause
        # Add the message
        return_object['error']['message'] = error_message
    else:
        # Add the Pulse status
        return_object['status'] = 'SUCCESS'
        # Add an empty error message
        return_object['error'] = None

    # Add any additional data
    if data:
        return_object['data'] = data
    else:
        return_object['data'] = None

    return return_object


def _create_fuzzy_matches(x, y):
    """
    Create fuzzy matches.
    
    :param str x: first string to compare
    :param str y: second string to compare
    :return: dict results: dictionary of fuzzy match results
    """
    r1 = fuzz.ratio(x, y)
    r2 = fuzz.token_sort_ratio(x, y)
    r3 = fuzz.token_set_ratio(x, y)
    r4 = fuzz.partial_ratio(x, y)
    r5 = fuzz.partial_token_sort_ratio(x, y)
    r6 = fuzz.partial_token_set_ratio(x, y)

    ratios = [r1, r2, r3, r4, r5, r6]
    ratio_average = mean(ratios)

    results = {
        "simple_ratio": r1,
        "token_sort_ratio": r2,
        "token_set_ratio": r3,
        "partial_ratio": r4,
        "partial_token_sort_ratio": r5,
        "partial_token_set_ratio": r6,
        "ratio_average": ratio_average
    }

    return results


def _answer_in_response(applicant_answer, acceptable_answer):
    """
    Determine if the entire acceptable answer is contained in the applicant's answer.
    
    :param str applicant_answer: the answer provided by the applicant
    :param str acceptable_answer: the answer to check against
    :return: boolean result: 100 if all parts are found in the response otherwise 0
    """
    # Determine if the acceptable answer parts are in the given answer
    acceptable_answer_parts = [x.lower() for x in acceptable_answer.split(" ")]
    answer_parts = [x.lower() for x in applicant_answer.split(" ")]

    answer_parts_found = list()

    for part in acceptable_answer_parts:
        if part in answer_parts:
            answer_parts_found.append("F")
        else:
            answer_parts_found.append("NF")

    if "NF" in answer_parts_found:
        return 0
    else:
        return 100


def score_job_application(application_questions, job_application):
    """
    Score a job application.
    
    :param application_questions: questions and their answers
    :param job_application: job application data
    :return: dict job application with scores and an accept/reject decision
    """
    # For each answer in the job application
    #   Get the approved answer, produce a score and the determine a final pass/fail
    # Return all scores and the final pass/fail to the calling method

    scored_app = deepcopy(job_application)

    pass_fails = list()

    for ja_response in scored_app['applicant_responses']:
        # Look up the answer in the application questions
        acceptable_answer = application_questions[ja_response['id']]

        # Create the fuzzy ratios and add them to the applicant's answer
        ja_response['fuzzy_ratios'] = _create_fuzzy_matches(ja_response['answer'], acceptable_answer)

        # Determine if the acceptable answer is in the answer provided
        ja_response['answer_in_response'] = _answer_in_response(applicant_answer=ja_response['answer'],
                                                                acceptable_answer=acceptable_answer)

        # Determine if this answer passes or fails
        if acceptable_answer.lower() == "any":
            pass_fails.append("P")
        elif ja_response['fuzzy_ratios']['partial_token_set_ratio'] >= 80:
            pass_fails.append("P")
        else:
            pass_fails.append("F")

    if "F" in pass_fails:
        scored_app['accepted'] = False
    else:
        scored_app['accepted'] = True

    return scored_app
