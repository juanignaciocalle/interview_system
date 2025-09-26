import pymongo
import os
import json
from bson import ObjectId
from bson.json_util import dumps

MONGO_URI = os.environ['MONGO_URI']
client = pymongo.MongoClient(MONGO_URI)
db = client['user_database']
users_collection = db.users

def handler(event, context):
    try:
        user_id_str = event['pathParameters']['userId']
        
        try:
            user_id = ObjectId(user_id_str)
        except Exception:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid user ID format'})
            }

        body = json.loads(event.get('body', '{}'))
        
        # Construir el objeto de actualización. Solo actualizamos campos presentes.
        update_fields = {}
        if 'name' in body:
            update_fields['name'] = body['name']
        if 'email' in body:
            update_fields['email'] = body['email']
        # Podrías añadir más campos aquí

        if not update_fields:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No fields to update provided'})
            }

        # Realizar la actualización en MongoDB
        result = users_collection.update_one(
            {'_id': user_id},
            {'$set': update_fields}
        )

        if result.matched_count == 0:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }

        # Opcional: devolver el usuario actualizado
        updated_user = users_collection.find_one({'_id': user_id})
        
        return {
            'statusCode': 200,
            'body': dumps(updated_user)
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }