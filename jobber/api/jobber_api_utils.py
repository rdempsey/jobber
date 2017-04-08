"""
jobber.api.jobber_api_utils
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Handy functions used by the Jobber API.

"""


def create_return_object(error_status=False, error_cause=None, error_message=None, data=None):
    """
    Create generic response objects. Complies with PULSE UI 3 SPEC.

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
