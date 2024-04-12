import logging


def log_response(response):
    """
    format the response and log it
    :param response:
    """
    headers = response.headers
    str_response = "Status code: %s\n" % response.status_code
    str_response += "%s\n" % ''.join("%s:%s\n" % (k, v) for k, v in headers.items())
    str_response += "Content: %s\n" % response.text
    logging.debug("Response: %s" % str_response)
