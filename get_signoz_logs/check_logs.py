import os, requests, json
from dotenv import load_dotenv

load_dotenv()


def load_headers():
    headers = {
        "Authorization": os.getenv("BEARER_TOKEN"),
    }

    return headers


def getBearerToken(env_type):
    with open("config/signoz_config.json") as f:
        config = json.load(f)

    if env_type == "production":
        url = config["prod_base_url"] + config["login_url"]
    else:
        url = config["non_prod_base_url"] + config["login_url"]

    payload = {
        "email": config["email"],
        "password": config["password"],
    }
    response = requests.post(url, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Failed to login to Signoz. Status code: {response.status_code}\n\n")
        print(response.text)
        return None
    else:
        response_json = response.json()
        bearer_token = f'Bearer {response_json.get("accessJwt")}'
        os.environ["BEARER_TOKEN"] = bearer_token
        return bearer_token


def store_log_in_json(logs):
    with open("logs/signoz_logs.json", "w") as f:
        json.dump(logs, f)


def check_signoz_logs(payload, env_type):
    with open("config/signoz_config.json") as f:
        config = json.load(f)

    if env_type == "production":
        url = config["prod_base_url"] + config["search_url"]
    else:
        url = config["non_prod_base_url"] + config["search_url"]

   
    # loading headers and payload for api calls
    headers = load_headers()

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()

    if response.status_code == 200:
        print("Successfully fetched data from Signoz")
        store_log_in_json(response_data)
        return response.json()
    else:
        if (response.status_code == 401) and (
            response_data["errorType"] == "unauthorized"
        ):
            bearer_token = getBearerToken(env_type)
            headers["Authorization"] = bearer_token
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            status_code = response.status_code
            if status_code != 200:
                print("Failed to fetch data from Signoz: ", response.json())
            else:
                response_data = response.json()
                print("Successfully fetched data from Signoz")
                store_log_in_json(response_data)
                return response_data
