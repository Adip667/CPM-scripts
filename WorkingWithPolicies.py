import urllib3 as urllib3
from utils import call_rest_endpoint, get_token, print_all

##########
### PLEASE UPDATE - required input for demo ###
##########

host = '1.1.1.1'  # used for all steps in the demo
api_key = '1f0240e8ce04bd378a7705d4b91f1cdcd1ef50324'  # used for step 1 to get access token
user = 3  # used in step 3 when listing the policies
account = 5  # used in step 3 when listing the policies
existing_policy_id = 2  # used in steps 5, 6 ,7 when getting policy details/future run time/backup targets
days_ahead = 3  # used in step 7 when getting future run times
policy_create_data = {  # used in step 8 when creating new policy
    'account': 1,# need to be updated with relevant ID
    'auto_remove_resource': 'N','description': 'my description','enabled': False, 'generations': 3,
    'name': 'policy_name2',
    'schedules': [5, 1]  # need to be updated with relevant schedule ID
}
policy_update_data = {  # used in step 9 when updating the newly created policy
    'description': 'my description updated',
    'enabled': True,
    'generations': 4,
    'name': 'policy_name_updated',
}
##########
##########

if __name__ == '__main__':
    URL_API = 'https://{}/api/'.format(host)  # updating the base URL with the provided Host
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print('\nRunning Example (created using: N2WS V4.0.0c, RESTful API Guide V2.0.0)')

    print('\nStep 1. Getting access token using API KEY and updating headers')
    tokens = get_token(URL_API, api_key)  # calling function to generate access token from the provided API key
    url = URL_API + 'token/obtain/api_key/'  # API Used: 38.1. Generate Access & Refresh tokens
    headers_json = {'Accept': 'application/json;', 'Authorization': 'Bearer {}'.format(tokens[0])}  # creating json header with the access token, will be used later for get API calls

    print('\nStep 2. Print a list of AWS policies')
    url = URL_API + 'aws/policies/'  # API Used: 10.2. List CPM policies
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print_all(responses)

    print('\nStep 3. Print a list of AWS policies again, but this time using filters - for example account/user')
    url = URL_API + 'aws/policies/?user={}&account={}'.format(user, account)  # API Used: 10.2. List CPM policies
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print_all(responses)

    print('\nStep 4. Print a list of Azure policies')
    url = URL_API + 'azure/policies/'  # API Used: 27.2. List Azure Policies
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print_all(responses)

    print('\nStep 5. Retrieve specific aws policy details for the id provided (EXISTING_POLICY_ID)')
    url = URL_API + 'aws/policies/{}/'.format(existing_policy_id)  # API Used: 10.3. Retrieve a CPM policy
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print(' {}'.format(responses))

    print('\nStep 6. List all targets associated with an AWS policy for the id provided (EXISTING_POLICY_ID)')
    url = URL_API + 'aws/policies/{}/targets/'.format(existing_policy_id)  # API Used: 10.30. List all the targets associated with a CPM policy
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print_all(responses)

    print('\nStep 7. List an AWS policy’s future scheduled run times for the id provided (EXISTING_POLICY_ID)')
    url = URL_API + 'aws/policies/{}/run_times/?days_ahead={}'.format(existing_policy_id,days_ahead)  # API Used: 10.30. List all the targets associated with a CPM policy
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print_all(responses)

    print('\nStep 8. Create AWS policy using the provided data')
    url = URL_API + 'aws/policies/'  # API Used: 10.1. Create a CPM policy
    responses = call_rest_endpoint(url=url, headers=headers_json, type='post',data=policy_create_data)  # create the policy with the data provided: POLICY_CREATE_DATA
    new_pol_id = responses['id']
    print(' {}'.format(responses))

    print('\nStep 9. Update the policy we created')
    url = URL_API + 'aws/policies/{}/'.format(new_pol_id)  # API Used: 10.4. Update a CPM policy
    responses = call_rest_endpoint(url=url, headers=headers_json, type='put',data=policy_update_data)  # update the policy with the data provided: POLICY_UPDATE_DATA
    print(' {}'.format(responses))  # responses contains the updated policy details

    print('\nStep 10. Delete the policy we created')
    url = URL_API + 'aws/policies/{}/'.format(new_pol_id)  # API Used: 10.5. Delete a CPM policy
    responses = call_rest_endpoint(url=url, headers=headers_json, type='delete')
    print(' {}'.format(responses)) # print the response code for the delete, http 204 = success
