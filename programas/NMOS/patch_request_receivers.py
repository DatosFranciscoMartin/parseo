import requests
import json

# URL del endpoint al que deseas hacer el PATCH
url = "http://sb-docker.medusa.csur:82/x-nmos/connection/v1.1/single/receivers/4e4ff99b-79fb-5e84-8b68-4beda8d63516/staged/"
#url = "http://172.29.226.11:8080/x-nmos/connection/v1.1/single/receivers/8f7f50c4-1c60-4089-bde3-b388627678f1/staged/"

objeto = {
    #"sender_id" : "e76710ce-2d31-52d5-a3a7-828756e5768b",
    "master_enable": True,
    "activation" : {
        "mode" : "activate_immediate"
    },
    "transport_params": [
        {
        #"connection_authorization": True,
        "connection_uri": "ws://172.29.226.16:8060",
        #"ext_is_07_rest_api_url": "http://10.0.1.3:80/x-nmos/events/v1.0/sources/e7cf41b1-599e-5bbf-a732-b5efaa9ebb52",
        #"ext_is_07_source_id": "e7cf41b1-599e-5bbf-a732-b5efaa9ebb52"
        }
        ]
}
# Encabezados de la solicitud (opcional, dependiendo de la API)
headers = {
    'Content-Type': 'application/json'
}

# Realizar la solicitud PATCH
respuesta = requests.patch(url, json=objeto, headers=headers)

jsonformateado = json.dumps(respuesta.json(), indent=4)

print(jsonformateado)