#!/bin/bash

echo "Example created using: N2WS V4.0.0c, RESTful API Guide V2.0.0"

### input for demo######
API_KEY='xxxxxxxxxxxxxxxxxxx'
HOST='10.192.xxx.xxx'
BACKUP_ID='280xxx'
##############


printf '\nStep 1.  Calling obtain token\n' # API used: 38.1. Generate Access & Refresh tokens
temp=$(curl -k -X POST https://$HOST/api/token/obtain/api_key/ -H 'Accept: application/json;' -H 'Content-Type: application/json' -d '{"api_key": "'"$API_KEY"'"}')
access_token=$(echo $temp  | jq .access | tr -d '"')
refresh_token=$(echo $temp  | jq .refresh | tr -d '"')
echo access token is $access_token
echo refresh token is $refresh_token

printf '\nStep 2.  list aws backup records\n' # API used: 6.1. List CPM backup records
temp=$(curl -k -X GET "https://$HOST/api/aws/backups/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name, start_time, status, policy}'

printf '\nStep 3.  list aws backup records with status=b filter (successful) and order by -start_time(descending order)\n'
temp=$(curl -k -X GET "https://$HOST/api/backups/?status=B&ordering=-start_time" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name, start_time, status, policy}'

printf '\nStep 4.  list policies and search (search=test), \n' # API used: 10.2. List CPM policies
temp=$(curl -k -X GET "https://$HOST/api/aws/policies/?search=test" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name, generations, copy_to_s3_enabled}'

printf '\nStep 5.  list schedules\n' # API used: 35.2. List CPM schedules
temp=$(curl -k -X GET "https://$HOST/api/schedules/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name, every_unit, every_how_many }'

printf '\nStep 6.  list accounts\n' # API used: 5.1. List CPM accounts
temp=$(curl -k -X GET "https://$HOST/api/aws/accounts/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name, is_dr_account}'

printf '\nStep 7.  list backup accounts\n' # API used: 5.3. List CPM backup accounts
temp=$(curl -k -X GET "https://$HOST/api/aws/accounts/backup/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name}'

printf '\nStep 8.  list snapshots\n' # API used: 6.5. List backup snapshots
temp=$(curl -k -X GET "https://$HOST/api/aws/backups/${BACKUP_ID}/snapshots/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, snapshot_id,status, region}'

printf '\nStep 9.  list s3_repositories\n' # API used: 17.2. List S3 repositories
temp=$(curl -k -X GET "https://$HOST/api/aws/s3_repositories/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name, aws_region}'
