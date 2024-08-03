import datetime
import urllib3 as urllib3
from utils import call_rest_endpoint, get_token

##########
### PLEASE UPDATE - required input for demo ###
##########
host = '1.1.1.1'  # used for all steps in the demo
api_key = '1f0240e8ce04bd378a7705d4b91f1cdcd1ef50324'  # used in step 1 to get access token
azure_account = 1  # used in step 4 for the azure snapshot report
period_type = 'W'  # used in step 5 for the summery report
period_length = 1  # used in step 5 for the summery report
##########
##########


if __name__ == '__main__':  # do stuff
    URL_API = 'https://{}/api/'.format(host)  # updating the base URL with the provided Host
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print('\nRunning Example (created using: N2WS V4.0.0c, RESTful API Guide V2.0.0)')

    print('\nStep 1. Getting access token using API KEY and updating headers')
    tokens = get_token(URL_API, api_key)  # calling function to generate access token from the provided API key
    url = URL_API + 'token/obtain/api_key/'  # API Used: 38.1. Generate Access & Refresh tokens
    headers_csv = {'Accept': 'text/csv;', 'Authorization': 'Bearer {}'.format(tokens[0])}  # creating csv header with the access token, will be used later for csv reports API calls
    headers_summery = {'Accept': '*/*;','Authorization': 'Bearer {}'.format(tokens[0])}  # creating */* header, will be used by pdf report in step 5

    print('\nStep 2. Get Audit report')
    url = URL_API + 'reports/audit/'  # API Used: 33.1. Audit report
    responses = call_rest_endpoint(url=url, headers=headers_csv, type='get', file=True)  # call api and get the report file
    print(' {} Created'.format(responses))  # responses will contain the file name

    print('\nStep 3. Get aws backup report report, with filter time filter(last 7 days)')
    to_date = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%SZ')
    from_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')  # calculate last 7 day date
    url = URL_API + 'reports/backups/?from_time={}&to_time={}'.format(from_date, to_date)  # API Used: 33.2. Backup report
    responses = call_rest_endpoint(url=url, headers=headers_csv, type='get', file=True)
    print(' {} Created\n'.format(responses))

    print('\nStep 4. Get azure snapshot report, with azure_account filter')
    url = URL_API + 'azure/reports/snapshots/?azure_account={}'.format(azure_account)  # API Used: 29.3. Snapshots report
    responses = call_rest_endpoint(url=url, headers=headers_csv, type='get', file=True)
    print(' {} Created\n'.format(responses))

    print('\nStep 5. Get azure summery report (pdf), with period_length filter')
    url = URL_API + 'azure/reports/summary/?period_type={}&period_length={}'.format(period_type,period_length)  # get summery report for the provided period, API Used: 29.4. Summary report
    responses = call_rest_endpoint(url=url, headers=headers_summery, type='get', file=True)  # call api with the headers_summery header.
    print(' {} Created\n'.format(responses))
