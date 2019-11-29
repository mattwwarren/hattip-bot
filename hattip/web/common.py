from urllib.parse import parse_qsl


def qsl_to_json(request_body):
    """ Transform form data tuples to json

    Arguments:
    request_body -- the processed body from aiohttp.web.Request
    """
    decoded_body = parse_qsl(request_body)
    decoded_json = {}
    for t in decoded_body:
        decoded_json[t[0]] = t[1]

    return decoded_json
