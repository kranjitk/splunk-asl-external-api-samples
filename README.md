## Amazon Security Lake Cross Account RAM External Permission API samples



### RAM CLI examples
##### Check if resource-shares and resource-share-invitations APIs work from the application instance. If the application policies are set properly, these shouldn't work and should give Access Denied errors
`aws ram get-resource-shares --resource-owner OTHER_ACCOUNTS`

`aws ram get-resource-share-invitations`

##### CLI to retrieve secrets. Substitute with your Secret id name. Based on how the resource policy set and calling application role, this CLI will get secret values or fail.

`aws secretsmanager get-secret-value --secret-id ASLSharedSecret2`

##### Example Output *(If permitted to retreive by secrets manager resource policy and application role identity policy)*

```
{
    "ARN": "arn:aws:secretsmanager:us-east-1:123456789012:secret:ASLSharedSecret1-BVCxXZ",
    "Name": "ASLSharedSecret1",
    "VersionId": "3aa69144-3b05-4ff6-89e0-47eda361181c",
    "SecretString": "{\"resource_share_name\":\"LakeFormation-V3-UKGDXY2WLU-SplunkExternalId\",\"accountid\":\"0000111122223333\"}",
    "VersionStages": [
        "AWSCURRENT"
    ],
    "CreatedDate": "2024-05-06T13:40:08.272000+00:00"
}
```
##### Example Output *(If NOT permitted to retreive by secrets manager resource policy AND application role identity policy)*
```
An error occurred (AccessDeniedException) when calling the GetSecretValue operation: User: arn:aws:sts::123456789012:assumed-role/AmazonSSMRoleForInstancesQuickSetup/i-xxxxxxxxxxxx is not authorized to perform: secretsmanager:GetSecretValue on resource: ASLSharedSecret2 with an explicit deny in a resource-based policy
```

##### Example Lambda invocations after retrieving the secrets. Substitute resource share name and sender account id values.

```bash
aws lambda invoke --function-name resource-share-api \
--payload '{"resource_share_name": "LakeFormation-V3-UKGDXY2WLU-SplunkExternalId","api_name": "get_resource_shares","accountid": "647604195155"}' \
--cli-binary-format raw-in-base64-out response.json
```

```bash
aws lambda invoke --function-name resource-share-api \
--payload '{"resource_share_name": "LakeFormation-V3-LRHBYSN8JR-gifty_acme","api_name": "get_resource_share_invitations","accountid": "410617500488"}' \
--cli-binary-format raw-in-base64-out response.json
```
##### Verify the output for retrieved json output
`cat response.json  | jq '.'`