__author__ = 'semyon'

from cent.core import Client
from cent.core import generate_channel_sign

import six
import time
import hmac
from hashlib import sha256

centrifuge_host = "http://127.0.0.1:8001"

web_secret = "strong_secret"

secret = "very-long-secret-key"

client = Client(centrifuge_host, secret)

def generate_token(secret, user, timestamp, info=""):
    sign = hmac.new(six.b(secret), digestmod=sha256)
    sign.update(six.b(user))
    sign.update(six.b(timestamp))
    sign.update(six.b(info))
    return sign.hexdigest()

def generate_channel_token(secret, user, info=""):
    channel_name = "$versionmonitor" + user
    print(channel_name)
    auth = hmac.new(six.b(str(secret)), digestmod=sha256)
    auth.update(six.b(str(client)))
    auth.update(six.b(str(channel_name)))
    auth.update(six.b(info))
    return auth.hexdigest()

def create_user_token(api_user):
    ms = str(int(time.time() * 1000.0))
    return generate_token(secret, api_user.push_id, ms), generate_channel_token(secret, api_user.push_id), ms


def send_push(message, push_id):
    params = {
        "watch": "true",
        "channel": "versionmonitor#" + push_id,
        "data": message,
        "client": push_id
    }
    client.add("publish", params)
    result, error = client.send()
    print(result)
    print(error)




