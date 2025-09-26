import pymongo
import os
import json
from bson import ObjectId
from bson.json_util import dumps


# Conexión a MongoDB (reutilizada entre invocaciones)
MONGO_URI = os.environ['MONGO_URI']
client = pymongo.MongoClient(MONGO_URI)
db = client['user_database']
users_collection = db.users


def handler(event, context):
    try:
        # Obtener el userId de los parámetros de la ruta
        user_id_str = event['pathParameters']['userId']
        # Convertir el string del ID a un ObjectId de MongoDB
        try:
            user_id = ObjectId(user_id_str)
        except Exception:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid user ID format'})
            }

        # Buscar el usuario en la base de datos
        user = users_collection.find_one({'_id': user_id})

        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }
        # bson.json_util.dumps maneja correctamente tipos de MongoDB como
        # ObjectId
        return {
            'statusCode': 200,
            'body': dumps(user)
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
