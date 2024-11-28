import requests
import yaml

response = requests.get("http://localhost:8080/apispec_1.json")
response.raise_for_status()  # This will raise an error if the request was unsuccessful

swagger_json = response.json()

swagger_yaml = yaml.dump(swagger_json, sort_keys=False)

with open("swagger.yaml", "w") as file:
    file.write(swagger_yaml)
