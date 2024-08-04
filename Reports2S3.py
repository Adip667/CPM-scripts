import requests
import urllib3
import re
from botocore.exceptions import ClientError
import boto3
import os
import datetime

def get_report(endpoint,to_date,from_date=None):
    URL_API_REPORT = URL_API + 'reports/' +endpoint
    url = URL_API_REPORT.format(host=host)
    authorization = HEADER_AUTHORIZATION.format(access_token=access_token)

    if from_date is not None:
        url = url + '?from_time={from_date}&to_time={to_date}'
        url = url.format(to_date=to_date,from_date=from_date)
        print(url)


    HEADER_ACCEPT = 'text/csv; version=1.7'
    headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}

    response = call_rest_endpoint(url=url, headers=headers,type='get')

    fname = re.findall("filename=(.+)", response.headers['Content-Disposition'])[0]
    fname =fname.replace('"','')

    with open(fname, "wb") as file:
        file.write(response.content)
    return fname

def GetServernameID():
    URL_API_REPORT = URL_API + 'settings/identifier/'
    url = URL_API_REPORT.format(host=host)
    authorization = HEADER_AUTHORIZATION.format(access_token=access_token)

    HEADER_ACCEPT = 'application/json; version=1.7'
    headers = {'Accept': HEADER_ACCEPT, 'Authorization': authorization}

    response = call_rest_endpoint(url=url, headers=headers,type='get')
    response_json = response.json()

    return response_json['cpm_name'] +'_'+ response_json['cpm_uuid']


def call_rest_endpoint(url,headers,type='post',data=None):
    """
    Handle all the calls to the CPM Rest endpoints
    :return:
    """
    VERIFY_SSL = False

    try:
        if type =='post':
            response = requests.post(url=url, headers=headers, data=data, verify=VERIFY_SSL)  # calling the API
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        elif type =='get':
            response = requests.get(url=url, headers=headers, verify=VERIFY_SSL)  # calling the API
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.

    except requests.exceptions.HTTPError as err:
        print(f"HTTPError: {err}\nHTTPError message:{err.response.text}\n")

    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")

    return response

def obtain_api_token(host,api_key):
    """
    Obtain `Access Token` and `Refresh Token` by using `API Authentication Key`.
    """
    url = URL_TOKEN_OBTAIN.format(host=host)
    headers = {'Accept': 'application/json; version=1.7'}
    data = {'api_key': api_key}

    response = call_rest_endpoint(url=url, headers=headers, data=data)
    response_json = response.json()

    return response_json['access'], response_json['refresh']

def upload_report_s3(path, bucketName,reporttype, filename):
    """
    Upload files to S3
    :param path: path to the file
    :param bucketName: bucket name to upload to
    :param filename: the file to upload
    """

    s3 = boto3.resource('s3')
    try:
        s3.meta.client.upload_file(path, bucketName,serverID + '/' + reporttype +'/' +filename)
    except ClientError as e:
        print(e)

if __name__ == '__main__':  # do stuff
    URL_API = "https://{host}/api/"
    URL_TOKEN_OBTAIN = URL_API + "token/obtain/api_key/"
    HEADER_AUTHORIZATION = "Bearer {access_token}"
    host= 'ec2-54-85-32-237.compute-1.amazonaws.com'
    bucket_name ='reportarchive-cpm'
    api_key= '1f020e8ce04bd378a7705d4b91fcdcdef50324b3ba4eee913f79e1265e17bb35637b20012966ae9944c81f62568cb8d0fbb5f529ff0f0321'
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    token = obtain_api_token(host,api_key)
    print(f'Access token is: {token[0]}\nRefresh toeken is: {token[1]}')
    access_token = token[0]

    reports =('snapshots','backups','audit')

    to_date = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%SZ')
    from_date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')

    serverID = GetServernameID()
    print(serverID)
    for reportType in reports:
        reportname = get_report(reportType,to_date,from_date)
        upload_report_s3(reportname, bucket_name,reportType, reportname)
        os.remove(reportname)
