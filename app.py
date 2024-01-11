from flask import Flask
import boto3
import json
import os
from datetime import datetime, timezone

app = Flask(__name__)

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', '')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
aws_region = os.environ.get('AWS_REGION', 'us-east-1')
elapsed_hours = int(os.environ.get('E_HOURS', 7 * 24))

iam_client = boto3.client('iam', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)


@app.route('/find', methods=['GET'])
def find_user():
    try:
        current_time = datetime.utcnow().replace(tzinfo=timezone.utc)

        response = iam_client.list_users()

        expired_users = []
        for user in response['Users']:
            for access_key in iam_client.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']:
                access_key_create_date = access_key['CreateDate'].replace(tzinfo=timezone.utc)

                if (current_time - access_key_create_date).total_seconds() > elapsed_hours * 3600:
                    expired_users.append({
                        'UserId': user['UserId'],
                        'AccessKeyId': access_key['AccessKeyId']
                    })

        response_data = {
            'current_time': str(current_time),
            'elapsed_hours': elapsed_hours,
            'expired_users': expired_users,
        }

        return json.dumps(response_data), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        return json.dumps({'error': str(e)}), 500, {'Content-Type': 'application/json'}


@app.route('/')
def hello_world():
    return 'Hello World!', 200


if __name__ == '__main__':
    app.run()
