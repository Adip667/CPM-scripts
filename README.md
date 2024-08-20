This repository contains various Python, Bash and Terraform scripts for N2WS product.


File name | Description
| ------------- |-------------
Utils.py | utility class for functions that are used in more then one example file, for example we have here the requests.post that handle the API calls for the various examples.
WorkingWithAPIKEY.py | General example, show how to use get token and refresh token
WorkingWithPolicies.py | General example, shows various API's for policies (get policy, list policy, list targets, create policy, update policy, delete policy)
WorkingWithRecovery.py | General example,  shows various API's for recovery (getting info and doing recovery)
WorkingWithReports.py | General example, shows various API's for Reports  (getting audit, backup and summery report)
CustomExcelReport(AWS).py | Scenario example, here we are collecting info from environment (policy list, account list, backups, recoveries, etc...) and printing it to one xlsx file
Reports2S3.py  | independent example, download various reports and upload them to AWS S3 report archive bucket, need to be run from EC2
Lambda_Report_To_S3.zip  | Lambda variant of the above Reports2S3.py, download various reports and upload them to AWS S3 report archive bucket
Using_APIKEY_ToGenerateTokens.sh | General Example, show how to call Obtain & refreash token from bash
VariousListApis.sh | General Example, show how to call list RestAPI's from bash
deploy_backup_server.tf | Terraform template to deploy N2WS server and configure with silent config(New_Deploy_SilentConfig.txt)
