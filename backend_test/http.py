import requests


def post(url: str,
         json: dict = None):
    r = requests.post(url=url, json=json, headers={
                      "content-type": "application/json"})

    r_status = r.status_code

    if r_status == 200:
        return r
