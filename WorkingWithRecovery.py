from utils import call_rest_endpoint, get_token
import time
import urllib3

##########
### Environment used: for this recovery demo i used
# 1 test aws policy with 2 linux instances
# 1 Recovery scenario for that same policy
# 1 test azure policy with 1 instance
##########
### PLEASE UPDATE - required input for demo ###
##########
host = '1.1.1.1'  # used for all steps in the demo
api_key = '1f0240e8ce04bd378a7705d4b91f1cdcd1ef50324'  # used in step 1 to get access token
instance_id = 'i-09c3bb1ca1de9a032'  # used in step 2 to get snapshot record id
backup_record_id = 280  # used in step 2,3 for the recovery
data_aws_backups_snapshots_instances_recover_create = { # used in step 3, overwrite some params for recovery for example new size or private IP
    'instance_type': 't3.small',
    'key_pair': 'CPM_Virginia',
    'vpc_assign_ip': '172.31.81.236'
}
azure_backup_record_id = 4  # used in step 4, 5, 6 for the recovery
azure_instance_id = '/subscriptions/f22899fac-7d9asb139fc1/resourceGroups/AVM_group/providers/Microsoft.Compute/virtualMachines/AVM'  # used in step 4, 5 for the recovery
data_azure_backups_snapshots_virtual_machines_recover_create = { # overwrite some params for recovery, used in step 5, 6 for the recovery
    'resource_group': 'AVM_group',
    'preserve_tags': True
}
recovery_scenario_id = 9  # used in step 6 to run recovery scenario
##########
##########

if __name__ == '__main__':  # do stuff
    URL_API = 'https://{}/api/'.format(host)  # updating the base URL with the provided Host
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print('\nRunning Example (created using: N2WS V4.0.0c, RESTful API Guide V2.0.0)')

    print('\nStep 1. Getting access token using API KEY and creating headers')
    tokens = get_token(URL_API, api_key)  # calling function to generate access token from the provided API key
    headers_json = {'Accept': 'application/json;', 'Authorization': 'Bearer {}'.format(tokens[0])}  # creating json header with the access token, will be used later for get API calls
    headers_csv = {'Accept': 'text/csv;', 'Authorization': 'Bearer {}'.format(tokens[0])}  # creating csv header with the access token, will be used later to get recovery log csv

    print('\nStep 2. Test recovery(AWS): first we need to get the snapshot record id for {} backup record {}'.format(instance_id,backup_record_id))  # to run step 3, we first need to get snap record id for the instance
    url = URL_API + 'aws/backups/{}/snapshots/instances/?resource={}'.format(backup_record_id, instance_id)  # adding resource={} to filter by instance ID ,API Used: 6.43. List all instances of a backup record
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')  # call the api
    print(f' {responses}')  # print the response for demo purpose

    print(f'\nStep 3. Test recovery(AWS): Now we can run recovery') # run recovery using snapshot record ID (responses[0].get('id'))
    url = URL_API + 'aws/backups/{}/snapshots/instances/{}/recover/'.format(backup_record_id, responses[0].get('id'))  # API Used: 6.48. Recover instance from backup
    responses = call_rest_endpoint(url=url, headers=headers_json, type='post', data=data_aws_backups_snapshots_instances_recover_create)
    for i in range(1, 9):  # recovery running, we need wait and check if/when finished
        if responses.get('status') == 'P':  # status p = in Progress
            print(' Waiting')
            time.sleep(10)  # wait 10 sec before checking again
            url = URL_API + 'aws/recoveries/{}/'.format(responses.get('id'))  # responses[id] will hold the recovery record id,  API Used: 12.2. Retrieve a CPM recovery record
            responses = call_rest_endpoint(url=url, headers=headers_json, type='get')  # get the recovery record again
        else:  # finished, can be successful or fail.
            print(' {}'.format(responses))  # print the response json
            break
    url = URL_API + 'aws/recoveries/{}/logs/'.format(responses.get('id'))  # API Used: 12.4. List the selected logs
    responses = call_rest_endpoint(url=url, headers=headers_csv, type='get', file=True)  # get the recovery log csv
    print(f' log file: {responses}')  # print file name

    print('\nStep 4. Test recovery(Azure): get snapshot record ID')  # similar to step 2, we need to get the relevant snapshot id
    url = URL_API + 'azure/backups/{}/snapshots/virtual_machines/?resource={}'.format(azure_backup_record_id, azure_instance_id.lower())  # API Used: 26.8. List all virtual machines of a backup record
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print(' {}'.format(responses))
    azure_snapshot_id = responses[0].get('id')  # saving the snapshot record id to be used later.
    data_azure_backups_snapshots_virtual_machines_recover_create['nic_subnet'] = responses[0].get('subnet')  # adding subnet details to the data that will be used for recovery

    print('\nStep 5. Test recovery(Azure): get VM volume record id')
    url = URL_API + 'azure/backups/{}/snapshots/disks/?resource={}'.format(azure_backup_record_id, azure_instance_id)  # API Used: 26.4. List the disk snapshots of a backup record
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
    print(' {}'.format(responses))
    disks = []  # will contain the disk data to be recovered
    for disk in responses:  # iterate over the response and append disk details if it is related to the VM we are trying to recover.
        if disk['virtual_machine_id'] == azure_instance_id.lower():
            disks.append({'id': disk['id'],'is_os_disk': disk['is_os_disk'],'name': disk['backed_up_resource_name']})
    data_azure_backups_snapshots_virtual_machines_recover_create['disks'] = disks  # add disks details to the data used for recovery
    print(f' Disks records:{disks}')  # print for demo purposes

    print('\nStep 6. Test recovery(Azure): run recovery')
    url = URL_API + 'azure/backups/{}/snapshots/virtual_machines/{}/recover/'.format(azure_backup_record_id, azure_snapshot_id)  # API Used: 26.10. Recover virtual machine from backup"
    responses = call_rest_endpoint(url=url, headers=headers_json, type='post', data=data_azure_backups_snapshots_virtual_machines_recover_create)  # recover
    for i in range(1, 9):  # we need to wait/check for recovery to complete
        if responses.get('status') == 'P':  # status p = in progress
            print(' Waiting')
            time.sleep(10)  # wait 10 sec before checking again
            url = URL_API + 'azure/recoveries/{}/'.format(responses.get('id'))  # check for latest status, API Used: 28.2. Retrieve a CPM recovery record
            responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
        else:  # finished, can be successful or failed
            print(' {}'.format(responses))
            break
    url = URL_API + 'azure/recoveries/{}/logs/'.format(responses.get('id'))  # get recovery csv logs, API Used: 28.4. List the selected logs
    responses = call_rest_endpoint(url=url, headers=headers_csv, type='get', file=True)
    print(' log file: {}'.format(responses))

    print('\nStep 6. Recovery Scenario(AWS): run recovery with dry_run_only=True')  # to disable dry run set below dry_run_only to False
    data_aws_recovery_scenarios_recover_create = {'backup_id': backup_record_id,'dry_run_only': True}  # create data for RS
    url = URL_API + 'aws/recovery_scenarios/{}/recover/'.format(recovery_scenario_id)  # API Used: 13.11. Run a CPM recovery scenario
    responses = call_rest_endpoint(url=url, headers=headers_json, type='post', data=data_aws_recovery_scenarios_recover_create)  # dry-run
    for i in range(1, 9):  # we need to wait/check for recovery to complete
        if responses.get('status') == 'P':  # p = in progress
            print(' Waiting')
            time.sleep(10)  # wait 10 sec before checking again
            url = URL_API + 'aws/recovery_scenarios/records/{}/'.format(responses.get('id'))  # API Used: 13.4. Retrieve a CPM recovery scenario record
            responses = call_rest_endpoint(url=url, headers=headers_json, type='get')
        else:  # finished
            print(' {}'.format(responses))
            break
    recovery_scenario_record = responses.get('id')  # save RS record id
    url = URL_API + 'aws/recovery_scenarios/records/{}/logs/'.format(recovery_scenario_record)  # API Used: 13.7. List of recovery scenario record logs.
    responses = call_rest_endpoint(url=url, headers=headers_csv, type='get',file=True)  # get recovery scenario csv logs
    print(' log file: {}'.format(responses))  # print file name
    url = URL_API + 'aws/recoveries/?recovery_scenario_record={}'.format(recovery_scenario_record)  # API Used: 12.1. List CPM recovery records
    responses = call_rest_endpoint(url=url, headers=headers_json, type='get')  # get recoveries related to the recovery scenario
    for recovery_id in responses:  # we will get csv logs also for each recovery record associated with the recovery scenario record
        url = URL_API + 'aws/recoveries/{}/logs/'.format(recovery_id.get('id'))  # API Used: 12.4. List the selected logs
        responses = call_rest_endpoint(url=url, headers=headers_csv, type='get', file=True)
        print(' log file: {}'.format(responses))
