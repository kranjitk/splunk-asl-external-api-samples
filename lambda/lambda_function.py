import boto3
from botocore.exceptions import ClientError
import json
import datetime

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

def lambda_handler(event, context):
    print("Event")
    print(event)
    print(context)
    """
    Retrieves resource shares and resource share invitations from AWS RAM,
    filters the results based on the resource share name, and returns the filtered results.
    """
    resource_share_name = event.get('resource_share_name')
    if not resource_share_name:
        return {
            'statusCode': 400,
            'body': 'Resource share name is required.'
        }

    ram_client = boto3.client('ram')

    resource_share_api = event.get('api_name')
    resource_share_accountid = event.get('accountid')
    if not resource_share_api:
        return {
            'statusCode': 400,
            'body': 'Resource share API name is required.'
        }    
    if resource_share_api == 'get_resource_shares':
        resource_shares = {}
        try:
            # Retrieve resource shares
            response = ram_client.get_resource_shares(
                resourceOwner='OTHER-ACCOUNTS',
                name=resource_share_name
                )
            if len(response['resourceShares']) > 0:
                if response['resourceShares'][0]['owningAccountId'] == resource_share_accountid:
                    resource_shares = json.dumps(response['resourceShares'],cls=DatetimeEncoder)
                
            if not resource_shares:
                return {
                    'statusCode': 200,
                    'body': {
                        'resourceShares': None
                    }
                }                
                
            else:                
                return {
                    'statusCode': 200,
                    'body': {
                        'resourceShares': json.loads(resource_shares)
                    }
                }

            
    
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return {
                'statusCode': 500,
                'body': f'Error {error_code}: {error_message}'
            }

    elif resource_share_api == 'get_resource_share_invitations':
        resource_share_invitations = []
        try:
        
            response = ram_client.get_resource_share_invitations(
                maxResults=100
            )
            for rec in response['resourceShareInvitations']:
                if (rec['resourceShareName'] == resource_share_name and rec['senderAccountId'] == resource_share_accountid) :
                    rec = json.dumps(rec,cls=DatetimeEncoder)
                    rec = json.loads(rec)
                    resource_share_invitations.append(rec)
            next_token = response.get('nextToken')
            while next_token:
                response = ram_client.get_resource_share_invitations(
                maxResults=100,
                nextToken=next_token)
                for rec in response['resourceShareInvitations']:
                    if rec['resourceShareName'] == resource_share_name:
                        rec = json.dumps(rec,cls=DatetimeEncoder)
                        rec = json.loads(rec)
                        resource_share_invitations.append(rec)
                next_token = response.get('nextToken')                    
                if not next_token:
                    break
           
            if not resource_share_invitations:
                return {
                    'statusCode': 200,
                    'body': {
                        'resourceShareInvitations': None
                    }
                }
            else:
                return {
                    'statusCode': 200,
                    'body': {
                        'resourceShareInvitations': resource_share_invitations
                    }
                }                
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return {
                'statusCode': 500,
                'body': f'Error {error_code}: {error_message}'
            }
            
    else:
        return {
            'statusCode': 400,
            'body': 'Resource share API name is invalid.Try again with Valid Name'
        }


        
        