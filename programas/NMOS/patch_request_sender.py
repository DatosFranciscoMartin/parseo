import requests
import json

# URL del endpoint al que deseas hacer el POST
url = "http://sb-docker.medusa.csur:82/x-nmos/connection/v1.1/single/senders/e76710ce-2d31-52d5-a3a7-828756e5768b/staged/"

objeto = {
    "activation": {
        "mode": "activate_immediate",
        #"requested_time": "2:0",
        #"activation_time": "1"
    }
}
# Encabezados de la solicitud (opcional, dependiendo de la API)
headers = {
    'Content-Type': 'application/json'
}

# Realizar la solicitud POST
respuesta = requests.patch(url, json=objeto, headers=headers)

jsonformateado = json.dumps(respuesta.json(), indent=4)

print(jsonformateado)

