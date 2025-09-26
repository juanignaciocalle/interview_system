import pymongo
import os
import json
from bson import ObjectId


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
        # Eliminar el usuario
        result = users_collection.delete_one({'_id': user_id})

        if result.deleted_count == 0:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }

        # Por convención, una eliminación exitosa devuelve un cuerpo vacío
        # con un código 204 (No Content) o un mensaje de éxito con 200.
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted successfully'})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
