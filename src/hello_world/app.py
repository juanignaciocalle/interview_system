import json


def handler(event, context):
    """
    Una función de prueba que no hace nada más que devolver un mensaje.
    No tiene dependencias externas.
    """
    print("¡La función HelloWorld fue invocada con éxito!")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hola desde la función de prueba!"
        }),
    }
