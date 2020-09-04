import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


# def auth():
#    return os.environ.get("BEARER_TOKEN")

BEARER_TOKEN = ""

def create_url():
    return "https://api.twitter.com/2/tweets/sample/stream?expansions=geo.place_id,author_id&place.fields=full_name,country_code&user.fields=location&tweet.fields=entities"


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers, stream=True)
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            print(json.dumps(json_response))
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )


def main():
    bearer_token = BEARER_TOKEN
    url = create_url()
    headers = create_headers(bearer_token)
    timeout = 0
    while True:
        connect_to_endpoint(url, headers)
        timeout += 1


if __name__ == "__main__":
    main()
    
    
  