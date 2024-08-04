#!/bin/bash

echo "Example created using: N2WS V4.0.0c, RESTful API Guide V2.0.0"

### input for demo######
API_KEY='111111111111'
HOST='1.1.1.1'
##############

printf '\nStep 1.  Calling obtain token\n' # API used: 38.1. Generate Access & Refresh tokens
temp=$(curl -k -X POST "https://$HOST/api/token/obtain/api_key/" -H 'Accept: application/json;' -H 'Content-Type: application/json' -d '{"api_key": "'"$API_KEY"'"}')
access_token=$(echo $temp  | jq .access | tr -d '"')
refresh_token=$(echo $temp  | jq .refresh | tr -d '"')
echo access token is $access_token
echo refresh token is $refresh_token

printf '\nStep 2.  Listing aws accounts\n' # API used: 5.1. List CPM accounts
temp=$(curl -k -X GET "https://$HOST/api/aws/accounts/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name}'

printf '\nStep 3.  let refresh the token\n' # API used: 38.2. Refresh an Access token
temp=$(curl -k -X POST "https://$HOST/api/token/refresh/" -H 'Accept: application/json;' -H 'Content-Type: application/json' -d '{"refresh": "'"$refresh_token"'"}')
refresh_token=$(echo $temp  | jq .refresh | tr -d '"')
echo new access token is $access_token

printf '\nStep 4.  Listing accounts\n' # API used: 5.1. List CPM accounts
temp=$(curl -k -X GET "https://$HOST/api/aws/accounts/" -H "Accept: application/json;" -H "Authorization: Bearer ${access_token}")
echo $temp | jq .''[] | jq '{id, name}'