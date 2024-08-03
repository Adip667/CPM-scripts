import re
import sys
import requests as requests

## utility class for functions that are used in more then one example file
def call_rest_endpoint(**kwargs):
    """
    Handle all the calls made by the various examples to the CPM Rest endpoints
    :param kwargs['url']: contain the API URL to call
    :param kwargs['headers']: the headers for the API call
    :param kwargs['data']: will contain additional data for post/put calls, for example details for creating a policy
    :param kwargs['type']: the type of call to do - post/put/delete/get
    :param kwargs['file']: Boolean, if true we are expecting a file, for example API call that returns CSV report
    """
    print(' Running call_rest_endpoint() -> {}'.format(kwargs['url']))  # print the URL that we are calling
    VERIFY_SSL = False

    try:
        if kwargs.get('type') == 'post':
            response = requests.post(url=kwargs['url'], headers=kwargs['headers'], json=kwargs['data'], verify=VERIFY_SSL)  # calling the API
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        elif kwargs.get('type') == 'put':
            response = requests.put(url=kwargs['url'], headers=kwargs['headers'], json=kwargs['data'], verify=VERIFY_SSL)  # calling the API
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        elif kwargs.get('type') == 'delete':
            response = requests.delete(url=kwargs['url'], headers=kwargs['headers'], verify=VERIFY_SSL)  # calling the API
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            return response
        else:  # get
            response = requests.get(url=kwargs['url'], headers=kwargs['headers'], verify=VERIFY_SSL)  # calling the API
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            if kwargs.get('file'):  # trying to get report or log file
                fname = re.findall('filename=(.+)', response.headers['Content-Disposition'])[0]  # get file name from response
                fname = fname.replace('"', '')  # remove " from the file name

                with open(fname, 'wb') as file:  # open/write the file
                    file.write(response.content)
                return fname  # return the created file name

    except requests.exceptions.HTTPError as err:  # Will likely catch any mistake in the API call, such as wrong parameters
        print('HTTPError: {} \ntext:{}'.format(err,err.response.text))
        sys.exit(1)  # should stop execution

    except requests.exceptions.RequestException as e:  # Will likely catch everything else
        print('RequestException: {}'.format(e))
        sys.exit(1)  # should stop execution

    return response.json()  # return the json response for API calls


def get_token(url_api, api_key):  # used in all examples to generate the access token for API calls
    url = url_api + 'token/obtain/api_key/'  # API Used: 38.1. Generate Access & Refresh tokens
    responses = call_rest_endpoint(url=url, headers={'Accept': 'application/json;'}, type='post',
                                   data={'api_key': api_key})
    tokens = responses['access'], responses['refresh']  # we will use the access token in all the other API's
    print(' Access token is: {}'.format(tokens[0]))  # print token for demo purposes
    return tokens

def print_all(response_json):
    for item in response_json: # printing for demo purposes
        print(' {}'.format(item))
