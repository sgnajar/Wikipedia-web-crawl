import requests

response = requests.get('https://en.wikipedia.org/wiki/https://en.wikipedia.org/wiki/Python_(programming_language)')

print(response.text)
