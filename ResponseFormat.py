def success(dict=None):
    response = {'success': True}
    if dict: response['payload'] = dict
    return response


def error(code, description, payload=None):
    response = {'success': False,
                'error': {
                    'code': code,
                    'message': description
                }}
    if payload: response['payload'] = payload
    return response
