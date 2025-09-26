import boto3
import os
import json
from botocore.client import Config

# Obtiene el nombre del bucket de la variable de entorno
BUCKET_NAME = os.environ['AVATAR_BUCKET_NAME']
s3_endpoint_url = os.environ.get('S3_ENDPOINT_URL')

s3_config = Config(
    s3={'addressing_style': 'path'},
    signature_version='s3v4'
)
s3_client = boto3.client(
    's3',
    endpoint_url=s3_endpoint_url,
    config=s3_config
)


def handler(event, context):
    try:
        user_id = event['pathParameters']['userId']
        object_key = f"avatars/{user_id}.jpg"
        
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_key, 'ContentType': 'image/jpeg'},
            ExpiresIn=3600
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'uploadUrl': presigned_url})
        }
    except Exception as e:
        print(e)
        return {'statusCode': 500, 'body': json.dumps({'error': 'Could not generate upload URL'})}
