import requests
from secret import key

webisteURL = 'https://www.google.com'
url = 'https://wave.webaim.org/api/request?key=' + key + '&url=' + webisteURL

r = requests.get(url)

print(r.text)
