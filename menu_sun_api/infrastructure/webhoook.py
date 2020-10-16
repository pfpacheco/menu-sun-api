import requests


class Webhook():

    @classmethod
    def notify(cls, url, payload, headers):
        return requests.post(url=url, json=payload,
                             headers=headers, verify=False)
