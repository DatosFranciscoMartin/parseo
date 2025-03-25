import requests
import json

# URL del endpoint al que deseas hacer el POST
url = "http://sb-docker.medusa.csur:82/x-nmos/connection/v1.1/single/receivers/a611b219-f85a-5900-8ddd-a3539b59082e/staged/"

objeto = {
    "sender_id" : "e76710ce-2d31-52d5-a3a7-828756e5768b",
    "master_enable": True,
    "activation" : {
        "mode" : "activate_immediate"
    },
    #"transport_params": [
    #{
    #    "destination_ip": "232.187.23.29",
    #    "destination_port": 5004,
    #    "rtp_enabled": True,
    #    "source_ip": "10.0.1.3",
    #    "source_port": 5004
    #    },
    #]
}
# Encabezados de la solicitud (opcional, dependiendo de la API)
headers = {
    'Content-Type': 'application/json'
}

# Realizar la solicitud POST
respuesta = requests.patch(url, json=objeto, headers=headers)

jsonformateado = json.dumps(respuesta.json(), indent=4)

print(jsonformateado)

