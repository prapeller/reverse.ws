import requests
import sys


def send_text_to_route(text):
    url = 'http://127.0.0.1:5006/tasks/'
    requests.post(url, json=text)


try:
    arg = sys.argv[1]
    send_text_to_route(arg)
except IndexError:
    print('enter argument to send to websocket')
except requests.exceptions.ConnectionError:
    print('run command "make build" to run services')

