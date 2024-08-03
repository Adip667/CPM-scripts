import urllib3 as urllib3
from utils import call_rest_endpoint, get_token,print_all

##########
### PLEASE UPDATE - required input for demo ###
##########
host = '1.1.1.1'  # used in all steps
root_user_api_key = '123456'  # used in step 1 to get access token
managed_user_api_key = '654321'  # used in step 3  to get access token
##########
##########

if __name__ == '__main__':

    URL_API = 'https://{}/api/'.format(host)  # updating the base URL with the provided Host
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print('\nRunning Example (created using: N2WS V4.0.0c, RESTful API Guide V2.0.0)')

    print('\nStep 1. Getting access token using API KEY and updating the headers')
    tokens = get_token(URL_API, root_user_api_key)  # calling function to generate access & refresh token from the provided Root user API key
    # tokens[0] contain the access token and tokens[1] the refresh token
    print(' Access tokens are valid for 1 hour by default and refresh token for 24 hours')
    print(' Access token is used for all others API calls, such list user, create policy etc.., while refresh token is used to generate new access token')
    headers_json = {'Accept': 'application/json;', 'Authorization': 'Bearer {}'.format(tokens[0])}  # creating json header with the access token

    print('\nStep 2. List accounts using the access token to, to show that it works')
    url = URL_API + 'aws/accounts/'  # API Used: 5.1. List CPM accounts
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print_all(responses)

    print('\nStep 3. Generate new tokens & print accounts, but this time with the managed user API Key')
    tokens_managed = get_token(URL_API, managed_user_api_key)  # calling function to generate access & refresh token, but now with the managed user API key
    headers_json_managed = {'Accept': 'application/json;', 'Authorization': 'Bearer {}'.format(tokens_managed[0])}  # creating another headers, this time with managed user token
    responses = call_rest_endpoint(url=url, headers=headers_json_managed, type='get')  # this will contain only the managed user accounts list, as we used the managed user access token
    print_all(responses)

    print('\nStep 4. If access token is expired, we can generate new one using the refresh token we have')
    url = URL_API + '/token/refresh/'  # refresh tokens are valid for 24 hours, this will generate only new access token, API Used: 38.2. Refresh an Access token
    tokens = (call_rest_endpoint(url=url, headers={'Accept': 'application/json;'}, type='post', data={'refresh': tokens[1]}), tokens[1])  # refreshing the root user access token and updating tokens param with access token(from func) & refresh(from tokens[1])
    print(' New access token is: {}'.format(tokens[0]))

    print(' Call list account again with new toekn, to show that it still works')
    url = URL_API + 'aws/accounts/'
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print_all(responses)
