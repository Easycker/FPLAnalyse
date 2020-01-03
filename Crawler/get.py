import requests

# Basic
r = requests.get('https://www.premierleague.com/players')
print(r.content)

# URL with parameter
payload = {'se':'274', 'cl':'1'}
r = requests.get('https://www.premierleague.com/players', params = payload)
print(r.url)