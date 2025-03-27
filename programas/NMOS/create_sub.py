import requests
import json

url = "http://sb-docker.medusa.csur/x-nmos/query/v1.3/subscriptions/"

objeto = {
    "max_update_rate_ms" : 100,
    "resource_path" : "/receivers",
    "params" : {
        "label" : "prueba"
    },
    "secure" : False,
    "persist" : True,
}

headers = {
    'Content-Type': 'application/json'
}

respuesta = requests.post(url, json=objeto, headers=headers)

jsonformateado = json.dumps(respuesta.json(), indent=4)

print(jsonformateado)