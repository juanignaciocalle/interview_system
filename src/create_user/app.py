import pymongo
import os
import json


# Obtiene la URI de la variable de entorno definida en template.yaml
MONGO_URI = os.environ['MONGO_URI']
client = pymongo.MongoClient(MONGO_URI)
db = client['user_database']


def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        name = body.get('name')
        email = body.get('email')

        if not name or not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Name and email are required'})
            }

        user_data = {
            'name': name,
            'email': email,
            'avatar_url': None
        }
        result = db.users.insert_one(user_data)
        return {
            'statusCode': 201,
            'body': json.dumps({'userId': str(result.inserted_id)})
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
